from django_filters import rest_framework as rest_filters
from rest_framework import filters, generics
from rest_framework.pagination import PageNumberPagination

from .models import Product, Category, Brand
from .serializers import ProductSerializer, CategorySerializer, BrandSerializer


class ListFilter(rest_filters.Filter):
    def filter(self, qs, value):
        return super().filter(qs, value.split(',')) if value else qs


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProductFilter(rest_filters.FilterSet):
    name = rest_filters.CharFilter(field_name="name", lookup_expr='icontains')
    category = ListFilter(field_name="category", lookup_expr='in')
    brand = ListFilter(field_name="brand", lookup_expr='in')
    min_price = rest_filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = rest_filters.NumberFilter(field_name="price", lookup_expr='lte')

    class Meta:
        model = Product
        fields = ('name', 'category', 'brand', 'min_price', 'max_price')


class ProductList(generics.ListAPIView):
    authentication_classes = []
    permission_classes = []
    pagination_class = StandardResultsSetPagination

    queryset = Product.objects.filter(is_deleted=False)
    serializer_class = ProductSerializer
    filter_backends = (filters.OrderingFilter, rest_filters.DjangoFilterBackend)
    ordering_fields = ('price', 'created_at')
    filterset_class = ProductFilter


class ProductDetail(generics.RetrieveAPIView):
    authentication_classes = []
    permission_classes = []

    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryList(generics.ListAPIView):
    authentication_classes = []
    permission_classes = []

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    # def get_queryset(self):
    #     product_filter = ProductFilter(self.request.GET, queryset=Product.objects.all())
    #     return Category.objects.filter(product__in=product_filter.qs).distinct()

    def get_serializer_context(self):
        product_filter = ProductFilter(self.request.GET, queryset=Product.objects.all())
        # Pass filter to serializer
        return {'product_filter': product_filter}


class BrandList(generics.ListAPIView):
    authentication_classes = []
    permission_classes = []

    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    # def get_queryset(self):
    #     product_filter = ProductFilter(self.request.GET, queryset=Product.objects.all())
    #     return Brand.objects.filter(product__in=product_filter.qs).distinct()

    def get_serializer_context(self):
        product_filter = ProductFilter(self.request.GET, queryset=Product.objects.all())
        # Pass filter to serializer
        return {'product_filter': product_filter}