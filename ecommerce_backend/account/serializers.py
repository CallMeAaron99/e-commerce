from rest_framework import serializers

from .models import User, Cart, Wishlist, Address, Order, OrderItem
from product.serializers import ProductSerializer
from product.models import Product


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'avatar')
    

    def get_avatar(self, obj):
        return obj.get_avatar()


class CartDetailSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = Cart
        fields = ('id', 'product', 'quantity')
    
    def validate_quantity(self, value):
        product = self.initial_data.get('product')
        product_instance = Product.objects.get(pk=product)
        if value > product_instance.stock:
            raise serializers.ValidationError("The quantity cannot exceed the product's stock.")
        return value


class CartListSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = ('id', 'product', 'quantity', 'created_at')


class WishlistDetailSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = Wishlist
        fields = ('id', 'product')


class WishlistListSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Wishlist
        fields = ('id', 'product', 'created_at')


class AddressListSerializer(serializers.ModelSerializer):
    country = serializers.SerializerMethodField()

    class Meta:
        model = Address
        fields = ('id', 'receiver', 'country', 'city', 'street', 'province', 'zip_code', 'phone', 'is_default', 'created_at')

    def get_country(self, obj):
        return obj.get_country_display()


class AddressDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = ('id', 'receiver', 'country', 'city', 'street', 'province', 'zip_code', 'phone', 'is_default')


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ('product', 'price', 'quantity')


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(read_only=True, many=True)
    country = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Order
        fields = ('id', 'items', 'receiver', 'country', 'city', 'street', 'province', 'zip_code', 'phone', 'sub_total', 'shipping', 'total', 'payment_type', 'status', 'created_at')

    def get_country(self, obj):
        return obj.get_country_display()

    def get_status(self, obj):
        return obj.get_status_display()



