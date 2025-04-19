from django.contrib import admin
from .models import Product, Order, OrderItem

# Register your models here.


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_id", "user", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user",)

    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
