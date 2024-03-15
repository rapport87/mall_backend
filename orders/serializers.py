from rest_framework import serializers
from .models import Order, OrderItem, OrderPayment
from products.models import Product
from django.db.models import Sum, F


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ["product_id", "product_name", "sale_price", "quantity", "thumbnail"]

    def get_thumbnail(self, obj):
        product = Product.objects.filter(id=obj.product_id).first()
        return product.thumbnail if product else None


class OrderPaymentSerializer(serializers.ModelSerializer):
    payment_display = serializers.CharField(
        source="get_payment_display", read_only=True
    )

    class Meta:
        model = OrderPayment
        fields = ["payment", "payment_display"]


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    order_id = serializers.IntegerField(source="id", read_only=True)
    first_product = serializers.SerializerMethodField()
    first_product_thumbnail = serializers.SerializerMethodField()
    total_product_price = serializers.SerializerMethodField()
    order_payment = OrderPaymentSerializer(read_only=True, many=True)

    class Meta:
        model = Order
        fields = [
            "order_id",
            "user_id",
            "username",
            "recipient_name",
            "recipient_tel",
            "address",
            "address_detail",
            "zip_code",
            "first_product",
            "first_product_thumbnail",
            "total_product_price",
            "created_at",
            "order_request",
            "order_items",
            "order_payment",
            "shipping_fee",
        ]

    def get_first_product(self, obj):
        order_items = obj.order_items.all()
        if order_items.exists():
            first_product_name = order_items[0].product_name
            additional_count = order_items.count() - 1
            if additional_count > 0:
                return f"{first_product_name} 외 {additional_count}개"
            return first_product_name
        return "상품 없음"

    def get_first_product_thumbnail(self, obj):
        order_items = obj.order_items.all()
        if order_items.exists():
            first_order_item = order_items[0]
            product = Product.objects.filter(id=first_order_item.product_id).first()
            return product.thumbnail if product else None

    def get_total_product_price(self, obj):
        total_price = obj.order_items.annotate(
            total_per_item=F("sale_price") * F("quantity")
        ).aggregate(total=Sum("total_per_item"))["total"]
        return total_price if total_price is not None else 0
