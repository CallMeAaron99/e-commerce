from rest_framework import serializers

from .models import Product, Category, Brand, ProductAttachment


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'product_count')

    def get_product_count(self, obj):
        product_filter = self.context.get('product_filter')

        if product_filter is not None:
            return Product.objects.filter(category=obj, id__in=product_filter.qs).count()
        else:
            return Product.objects.filter(category=obj).count()


class BrandSerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()
    logo = serializers.SerializerMethodField()

    class Meta:
        model = Brand
        fields = ('id', 'name', 'logo', 'product_count')

    def get_logo(self, obj):
        return obj.get_logo()

    def get_product_count(self, obj):
        product_filter = self.context.get('product_filter')

        if product_filter is not None:
            return Product.objects.filter(brand=obj, id__in=product_filter.qs).count()
        else:
            return Product.objects.filter(brand=obj).count()


class ProductAttachmentSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ProductAttachment
        fields = ('id', 'image')
    
    def get_image(self, obj):
        return obj.get_image()


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    attachments = ProductAttachmentSerializer(read_only=True, many=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'category', 'brand', 'price', 'discount_price', 'stock', 'attachments', 'sales', 'created_at', 'is_deleted')
