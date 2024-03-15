from rest_framework import serializers
from .models import Cart
from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "sale_price",
            "shipping_fee",
            "thumbnail",
        ]


class CartSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), write_only=True
    )
    product = ProductSerializer(read_only=True)
    quantity = serializers.IntegerField(default=1)  # 수량 필드 추가

    class Meta:
        model = Cart
        fields = [
            "id",
            "product",
            "product_id",
            "quantity",
        ]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        product = validated_data.pop("product_id")
        cart = Cart.objects.create(**validated_data, product=product)
        return cart
