from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Product
from categories.models import Category


class ProductTests(APITestCase):
    def setUp(self):
        # 테스트에 필요한 카테고리 및 상품을 미리 생성합니다.
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Laptop",
            description="A powerful laptop",
            price=1000,
            stock=10,
            category=self.category,
        )

    def test_view_products(self):
        """
        Products 뷰의 GET 요청을 테스트합니다.
        """
        url = reverse("products-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_product(self):
        """
        Products 뷰의 POST 요청을 테스트합니다.
        """
        url = reverse("products-list")
        data = {
            "name": "Smartphone",
            "description": "A new smartphone",
            "price": 500,
            "stock": 15,
            "category": self.category.id,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_view_product_detail(self):
        """
        ProductDetail 뷰의 GET 요청을 테스트합니다.
        """
        url = reverse("product-detail", args=[self.product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_product_detail(self):
        """
        ProductDetail 뷰의 PUT 요청을 테스트합니다.
        """
        url = reverse("product-detail", args=[self.product.id])
        data = {
            "name": "Updated Laptop",
            "description": "An updated powerful laptop",
            "price": 1100,
            "stock": 5,
            "category": self.category.id,
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
