from django.contrib import admin

from .models import Product, ProductAttachment, Brand, Category

class ProductAttachmentInline(admin.TabularInline):
    model = ProductAttachment


class ProductAdmin(admin.ModelAdmin):
    inlines = (ProductAttachmentInline, )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Product, ProductAdmin)
admin.site.register(Brand)
admin.site.register(Category)