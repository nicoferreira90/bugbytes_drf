from django.urls import path
from .views import ProductDetailView, OrderListView, UserOrderListView, ProductListCreateView

urlpatterns = [
    path("products/", ProductListCreateView.as_view(), name="product_list"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("orders/", OrderListView.as_view(), name="order_list"),
    path("user-orders/", UserOrderListView.as_view(), name="user_order_list"),
]
