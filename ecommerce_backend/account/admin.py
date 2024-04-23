from django.contrib import admin

from .models import User, Order

class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', )

admin.site.register(User)
admin.site.register(Order, OrderAdmin)
