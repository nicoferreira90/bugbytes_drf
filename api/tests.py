from django.test import TestCase
from .models import CustomUser, Product, Order, OrderItem
from django.urls import reverse


class UserOrderTestCase(TestCase):
    def setUp(self):
        # Set up your test data here
        self.user = CustomUser.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            price=10.00,
            stock=100,
            image="path/to/image.jpg",
        )
        self.order = Order.objects.create(
            user=self.user, status=Order.OrderStatus.PENDING
        )
        OrderItem.objects.create(order=self.order, product=self.product, quantity=2)

    def test_user_order_list(self):
        # Test the user order list view
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("user_order_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, "Test Product"
        )  # Check if the product is in the response

    def test_user_order_list_only_own_orders(self):
        # Test that the user can only see their own orders
        another_user = CustomUser.objects.create_user(
            username="anotheruser", password="anotherpassword"
        )
        another_order = Order.objects.create(
            user=another_user, status=Order.OrderStatus.PENDING
        )
        OrderItem.objects.create(order=another_order, product=self.product, quantity=1)

        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("user_order_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Product")
        self.assertNotContains(
            response, "anotheruser"
        )  # Check that the other user's order is not in the response

    def test_unauthenticated_user_order_list(self):
        # Test the user order list view for unauthenticated users. should return 403
        response = self.client.get(reverse("user_order_list"))
        self.assertEqual(response.status_code, 403)
