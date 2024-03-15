from rest_framework import serializers
from .models import Category
from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "pk",
            "name",
            "price",
            "sale_price",
            "shipping_fee",
            "thumbnail",
            "categories",
            "display_status",
        )


class CategoryProductsSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["products"]
