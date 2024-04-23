from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from account import views

urlpatterns = [
    path('me', views.me, name='me'),
    path('signup', views.signup, name='signup'),
    path('login', TokenObtainPairView.as_view(), name='token_obtain'),
    path('refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('edit-profile', views.editProfile, name='edit_profile'),
    path('edit-password', views.editPassword, name='edit_password'),
    path('password_reset', views.resetPassword, name="password_reset"),
    path('cart', views.CartList.as_view(), name="cart_list"),
    path('cart/<uuid:pk>', views.CartDetail.as_view(), name="cart_detail"),
    path('wishlists', views.WishlistList.as_view(), name="wishlist_list"),
    path('wishlists/<uuid:pk>', views.WishlistDetail.as_view(), name="wishlist_detail"),
    path('addresses', views.AddressList.as_view(), name="address_list"),
    path('addresses/<uuid:pk>', views.AddressDetail.as_view(), name="address_detail"),
    path('orders/', views.OrderList.as_view(), name="order_list"),
    path('orders/<uuid:pk>', views.OrderDetail.as_view(), name="order_detail"),
    path('order_cancel/<uuid:pk>', views.orderCancel, name="order_cancel"),
    path('checkout', views.checkout, name="checkout"),
    path('countries', views.getCountries, name="country_list"),
]