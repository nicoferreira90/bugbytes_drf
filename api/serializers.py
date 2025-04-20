from rest_framework import serializers
from .models import Product, Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "name",
            "description",
            "price",
            "stock",
        )

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be a positive number.")
        return value


class OrderItemSerializer(serializers.ModelSerializer):

    product_name = serializers.CharField(source="product.name", read_only=True)
    product_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, source="product.price", read_only=True
    )

    class Meta:
        model = OrderItem
        fields = (
            "product_name",
            "product_price",
            "quantity",
        )


class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(method_name="get_total_price")

    def get_total_price(self, obj):
        order_items = obj.items.all()
        total_price = sum(order_items.total_price for order_items in order_items)
        return total_price

    class Meta:
        model = Order
        fields = (
            "order_id",
            "created_at",
            "status",
            "user",
            "items",
            "total_price",
        )
