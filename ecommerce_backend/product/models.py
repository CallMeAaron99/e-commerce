import uuid

from django.db import models
from django.conf import settings

from account.models import User


class Category(models.Model):

    class Meta:
        db_table = 'category'
        verbose_name = '类型'
        verbose_name_plural = verbose_name

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True, verbose_name='名称')

    def __str__(self) -> str:
        return self.name


class Brand(models.Model):

    class Meta:
        db_table = 'brand'
        verbose_name = '品牌'
        verbose_name_plural = verbose_name
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True, verbose_name='名称')
    logo = models.ImageField(upload_to='brand_logo', verbose_name='Logo')

    def __str__(self) -> str:
        return self.name

    def get_logo(self):
        if self.logo:
            return settings.WEBSITE_URL + self.logo.url
        return ''


class Product(models.Model):

    class Meta:
        db_table = 'product'
        verbose_name = '商品'
        verbose_name_plural = verbose_name
        ordering = ('-created_at', )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, verbose_name='名称')
    description = models.TextField(blank=True, null=True, verbose_name='描述')
    category = models.ForeignKey(Category, related_name='product_category', on_delete=models.PROTECT, verbose_name='类型')
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, verbose_name='品牌')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格')
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='折扣价')
    stock = models.PositiveIntegerField(default=1, verbose_name='库存')
    sales = models.PositiveIntegerField(default=0, editable=False, verbose_name='销量')

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE, editable=False)

    is_deleted = models.BooleanField(default=False, verbose_name='下架')

    def __str__(self) -> str:
        return self.name


class ProductAttachment(models.Model):

    class Meta:
        db_table = 'product_attachments'
        verbose_name = '商品附件'
        verbose_name_plural = verbose_name
        ordering = ('order',)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='product_images', verbose_name='图片')
    product = models.ForeignKey(Product, related_name='attachments', on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField(default=1, verbose_name='顺序')

    def get_image(self):
        if self.image:
            return settings.WEBSITE_URL + self.image.url
        return ''
    
    def __str__(self) -> str:
        return str(self.image)