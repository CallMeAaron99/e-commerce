from django.urls import path

from product import views

urlpatterns = [
    path('', views.ProductList.as_view(), name='product_list'),
    path('<uuid:pk>', views.ProductDetail.as_view(), name='product_detail'),
    path('categories', views.CategoryList.as_view(), name='category_list'),
    path('brands', views.BrandList.as_view(), name='brand_list'),
]