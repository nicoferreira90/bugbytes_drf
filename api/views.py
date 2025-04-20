from django.http import JsonResponse
from rest_framework import generics, permissions, views
from api.serializers import ProductSerializer, OrderSerializer
from api.models import Product, Order
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderListView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related("items").all()
    serializer_class = OrderSerializer


class UserOrderListView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related("items").all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(user=user)
