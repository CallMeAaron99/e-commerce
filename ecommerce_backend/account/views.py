from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.http import Http404, HttpResponse
from django.conf import settings
from django.db import transaction
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from product.models import Product

from .forms import SignupForm, ProfileForm
from .models import COUNTRY_CHOICES, Address, Cart, Order, OrderItem, User, Wishlist
from .serializers import (
    AddressDetailSerializer,
    AddressListSerializer,
    CartDetailSerializer,
    CartListSerializer,
    OrderSerializer,
    UserSerializer,
    WishlistDetailSerializer, 
    WishlistListSerializer
)


@api_view(['GET'])
def me(request):
    serializer = UserSerializer(request.user)

    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    data = request.data

    form = SignupForm({
        'email': data.get('email'),
        'name': data.get('name'),
        'password1': data.get('password1'),
        'password2': data.get('password2'),
    })

    if form.is_valid():
        user = form.save()

        url = f'{settings.WEBSITE_URL}/account-activate/?email={user.email}&id={user.id}'

        # Send verification email
        send_mail(
            "激活账号",
            f"点击链接激活账号：{url}",
            settings.FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        return Response(status=status.HTTP_201_CREATED)

    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def editProfile(request):

    user = request.user
    email = request.data.get('email')

    if User.objects.exclude(id=user.id).filter(email=email).exists():
        return Response(status=409)
    else:
        form = ProfileForm(request.POST, request.FILES, instance=user)
        
        if form.is_valid():
            form.save()
        
        serializer = UserSerializer(user)
    
    return Response(serializer.data)


@api_view(['PUT'])
def editPassword(request):

    user = request.user
    form = PasswordChangeForm(data=request.POST, user=user)

    if form.is_valid():
        form.save()
    else:
        return Response(form.errors.as_json(), status=status.HTTP_400_BAD_REQUEST)
    
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def resetPassword(request):
    form = PasswordResetForm(request.data)

    if form.is_valid():
        form.save(use_https=request.is_secure(), from_email=settings.FROM_EMAIL, request=request)
    else:
        return Response(form.errors.as_json(), status=status.HTTP_400_BAD_REQUEST)
    
    return Response(status=status.HTTP_200_OK)


def accountActivate(request):
    email = request.GET.get('email')
    id = request.GET.get('id')

    if email and id:
        user = User.objects.get(id=id, email=email)
        user.is_active = True
        user.save()
    
    return HttpResponse("账号已激活")


@api_view(['GET'])
def getCountries(request):
    return Response(dict(COUNTRY_CHOICES))


@api_view(['PUT'])
@transaction.atomic
def orderCancel(request, pk):
    order = Order.objects.get(pk=pk)

    try:
        for order_item in OrderItem.objects.filter(order=order):
            # Restore product stock and sales
            product = Product.objects.get(pk=order_item.product.id)
            product.stock += order_item.quantity
            product.sales -= order_item.quantity
            product.save()

        # Set order status = Canceled
        order.status = 0
        order.save()
    except Exception as e:
        # Log the exception and return a 500 response
        print(f"An error occurred: {e}")
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@transaction.atomic
def checkout(request):
    address = Address.objects.get(pk=request.data['address'])
    cart_qs = Cart.objects.filter(created_by=request.user)

    # Insert order
    order = Order(
        receiver=address.receiver,
        country=address.country,
        city=address.city,
        street=address.street,
        province=address.province,
        zip_code=address.zip_code,
        phone=address.phone,
        shipping=request.data['shipping'],
        payment_type=request.data['payment_type'],
        created_by=request.user,
    )
    try:
        order.save()
        sub_total = 0
        
        for cart in cart_qs:
            # Update product stock and sales
            product = Product.objects.get(pk=cart.product.id)
            product.stock -= cart.quantity
            product.sales += cart.quantity
            product.save()

            # Insert order item
            order_item = OrderItem(
                product=cart.product,
                price=cart.product.price,
                quantity=cart.quantity,
                order=order
            )
            sub_total += order_item.price * order_item.quantity
            order_item.save()
            
        # Update order
        order.sub_total = sub_total
        order.total = float(sub_total) + order.shipping
        order.save()

        # Clean cart
        cart_qs.delete()
    except Exception as e:
        # Log the exception and return a 500 response
        print(f"An error occurred: {e}")
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(status=status.HTTP_200_OK)


class CartList(APIView):

    def get(self, request, format=None):
        cart = Cart.objects.filter(created_by=request.user)
        serializer = CartListSerializer(cart, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):

        try:
            # Product exists in cart
            serializer = CartDetailSerializer(
                Cart.objects.get(product=request.data['product'], created_by=request.user),
                data=request.data
            )
        except Cart.DoesNotExist:
            serializer = CartDetailSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartDetail(APIView):

    def get_object(self, pk):
        try:
            return Cart.objects.get(pk=pk)
        except Cart.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        cart = self.get_object(pk)
        serializer = CartDetailSerializer(cart, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        cart = self.get_object(pk)
        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WishlistList(APIView):

    def get(self, request, format=None):
        wishlist = Wishlist.objects.filter(created_by=request.user)
        serializer = WishlistListSerializer(wishlist, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = WishlistDetailSerializer(data=request.data)
        if serializer.is_valid():

            if not Wishlist.objects.filter(product=request.data['product'], created_by=request.user).exists():
                serializer.save(created_by=request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WishlistDetail(APIView):

    def get_object(self, pk):
        try:
            return Wishlist.objects.get(pk=pk)
        except Wishlist.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        wishlist = self.get_object(pk)
        wishlist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddressList(APIView):

    def get(self, request, format=None):
        address = Address.objects.filter(created_by=request.user)
        serializer = AddressListSerializer(address, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AddressDetailSerializer(data=request.data)
        if serializer.is_valid():
            if request.data['is_default']:
                # Set as default address
                Address.objects.filter(created_by=request.user).update(is_default=False)
            
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddressDetail(APIView):

    def get_object(self, pk):
        try:
            return Address.objects.get(pk=pk)
        except Address.DoesNotExist:
            raise Http404
        
    def get(self, request, pk, format=None):
        address = self.get_object(pk)
        serializer = AddressDetailSerializer(address)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        address = self.get_object(pk)
        serializer = AddressDetailSerializer(address, data=request.data)
        if serializer.is_valid():
            if request.data['is_default']:
                # Set as default address
                Address.objects.filter(created_by=request.user).update(is_default=False)
                
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        address = self.get_object(pk)
        address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderList(APIView):

    def get(self, request, format=None):
        order = Order.objects.filter(created_by=request.user)
        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data)


class OrderDetail(APIView):

    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            raise Http404
        
    def get(self, request, pk, format=None):
        order = self.get_object(pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        order = self.get_object(pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

