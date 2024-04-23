import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.conf import settings
from django.utils import timezone


COUNTRY_CHOICES = (
    ('Australia', '澳大利亚'),
    ('Belarus', '白俄罗斯'),
    ('Belgium', '比利时'),
    ('Brazil', '巴西'),
    ('Canada', '加拿大'),
    ('Chile', '智利'),
    ('China', '中国'),
    ('Estonia', '爱沙尼亚'),
    ('Finland', '芬兰'),
    ('France', '法国'),
    ('Germany', '德国'),
    ('Greece', '希腊'),
    ('Guatemala', '危地马拉'),
    ('Haiti', '海地'),
    ('Hungary', '匈牙利'),
    ('Iceland', '冰岛'),
    ('India', '印度'),
    ('Ireland', '爱尔兰'),
    ('Italy', '意大利'),
    ('Japan', '日本'),
    ('Mexico', '墨西哥'),
    ('Montenegro', '黑山'),
    ('Netherlands', '荷兰'),
    ('Norway', '挪威'),
    ('Peru', '秘鲁'),
    ('Russia', '俄罗斯'),
    ('South Korea', '韩国'),
    ('Spain', '西班牙'),
    ('Sweden', '瑞典'),
    ('Switzerland', '瑞士'),
    ('United Kingdom', '英国'),
    ('United States', '美国'),
)


class CustomUserManager(UserManager):

    def _create_user(self, name, email, password, **extra_fields):
        if not email:
            raise ValueError("You have not provided a valid e-mail address")
        
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_user(self, name=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(name, email, password, **extra_fields)
    
    def create_superuser(self, name=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(name, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    class Meta:
        db_table = 'user'
        verbose_name = '账号'
        verbose_name_plural = verbose_name

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, verbose_name='邮箱')
    name = models.CharField(max_length=50, blank=True, default='', verbose_name='用户名')
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True, verbose_name='头像')

    is_active = models.BooleanField(default=False, verbose_name='已激活')
    is_superuser = models.BooleanField(default=False, verbose_name='超级用户')
    is_staff = models.BooleanField(default=False, verbose_name='员工')

    date_joined = models.DateTimeField(default=timezone.now, verbose_name='注册日期')
    last_login = models.DateTimeField(blank=True, null=True, verbose_name='最近一次登录')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []


    def get_avatar(self):
        if self.avatar:
            return settings.WEBSITE_URL + self.avatar.url
        
        return 'https://www.milton.edu/wp-content/uploads/2019/11/avatar-placeholder.jpg'


class Cart(models.Model):
    class Meta:
        db_table = 'cart'
        verbose_name = '购物车'
        verbose_name_plural = verbose_name
        ordering = ('-created_at', )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey('product.Product', related_name='cart_product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='added_cart', on_delete=models.CASCADE)


class Wishlist(models.Model):
    class Meta:
        db_table = 'wishlist'
        verbose_name = '收藏'
        verbose_name_plural = verbose_name
        ordering = ('-created_at', )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # name = models.CharField(max_length=50)
    product = models.ForeignKey('product.Product', related_name='wishlist_product', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='created_wishlist', on_delete=models.CASCADE)


class Address(models.Model):
    class Meta:
        db_table = 'address'
        verbose_name = '用户地址'
        verbose_name_plural = verbose_name
        ordering = ('-created_at', )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    receiver = models.CharField(max_length=50, verbose_name='收货人')
    country = models.CharField(max_length=50, choices=COUNTRY_CHOICES, verbose_name='国家')
    city = models.CharField(max_length=50, verbose_name='市区')
    street = models.CharField(max_length=100, verbose_name='街道')
    province = models.CharField(max_length=50, verbose_name='省')
    zip_code = models.CharField(max_length=20, verbose_name='邮政编码')
    phone = models.CharField(max_length=20, verbose_name='手机')
    is_default = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='created_address', on_delete=models.CASCADE)


class Order(models.Model):
    class Meta:
        db_table = 'order'
        verbose_name = '订单'
        verbose_name_plural = verbose_name
        ordering = ('-created_at', )

    PAYMENT_CHOICES = (
        (0, '在线支付'),
        (1, '信用卡/储蓄卡'),
        (2, '货到付款'),
        (3, '其他'),
    )

    STATUS_CHOICES = (
        (0, '已取消'),
        (1, '已支付'),
        (2, '准备配送'),
        (3, '配送中'),
        (4, '已完成'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    receiver = models.CharField(max_length=50, verbose_name='收货人')
    country = models.CharField(max_length=50, choices=COUNTRY_CHOICES, verbose_name='国家')
    city = models.CharField(max_length=50, verbose_name='市区')
    street = models.CharField(max_length=100, verbose_name='街道')
    province = models.CharField(max_length=50, verbose_name='省')
    zip_code = models.CharField(max_length=20, verbose_name='邮政编码')
    phone = models.CharField(max_length=20, verbose_name='手机')
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='小计')
    shipping = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='运费')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='总计')
    payment_type = models.PositiveSmallIntegerField(choices=PAYMENT_CHOICES, default=0, verbose_name='支付方式')
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1, verbose_name='订单状态')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='下单日期')
    created_by = models.ForeignKey(User, related_name='created_order', on_delete=models.CASCADE, editable=False)

    def __str__(self) -> str:
        return str(self.id)


class OrderItem(models.Model):
    class Meta:
        db_table = 'order_items'

    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('product.Product', related_name='items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

