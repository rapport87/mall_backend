from django.contrib import admin
from django import forms
from .models import Order, OrderItem, OrderPayment
from users.models import User
from products.models import Product
from django.db.models import Sum, F


class OrderForm(forms.ModelForm):
    get_user = forms.ModelChoiceField(
        queryset=User.objects.all(), label="Username", to_field_name="id"
    )

    class Meta:
        model = Order
        fields = [
            "get_user",
            "shipping_fee",
            "recipient_name",
            "recipient_tel",
            "address",
            "address_detail",
            "zip_code",
        ]

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["get_user"].initial = self.instance.user_id

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user_id = self.cleaned_data["get_user"].id
        instance.username = self.cleaned_data["get_user"].username
        if commit:
            instance.save()
        return instance


class OrderAdmin(admin.ModelAdmin):
    form = OrderForm
    list_display = [
        "order_id",
        "get_first_product",
        "total_product_price",
        "recipient_name",
        "recipient_tel",
        "address",
        "address_detail",
        "zip_code",
    ]
    search_fields = ["id"]

    def order_id(self, obj):
        return obj.id

    order_id.short_description = "주문번호"

    def get_first_product(self, obj):
        order_items = obj.order_items.all()
        if order_items.exists():
            first_product_name = order_items[0].product_name
            additional_count = order_items.count() - 1
            if additional_count > 0:
                return f"{first_product_name} 외 {additional_count}개"
            return first_product_name
        return "상품 없음"

    get_first_product.short_description = "주문상품"

    def total_product_price(self, obj):
        total_price = obj.order_items.annotate(
            total_per_item=F("sale_price") * F("quantity")
        ).aggregate(total=Sum("total_per_item"))["total"]
        return total_price if total_price is not None else 0

    total_product_price.short_description = "총 상품 가격"


admin.site.register(Order, OrderAdmin)


class OrderItemForm(forms.ModelForm):
    get_product = forms.ModelChoiceField(
        queryset=Product.objects.all(), label="Product Name", to_field_name="id"
    )
    order = forms.ModelChoiceField(queryset=Order.objects.all(), label="Order")

    class Meta:
        model = OrderItem
        fields = ["order", "get_product", "sale_price", "quantity"]

    # product의 콤보박스 내용 저장처리 id -> Product.pk , product_name -> Product.name
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.product_id = self.cleaned_data["get_product"].id
        instance.product_name = self.cleaned_data["get_product"].name
        if commit:
            instance.save()
        return instance


class OrderItemAdmin(admin.ModelAdmin):
    form = OrderItemForm
    list_display = [
        "order_id",
        "get_product_display",
        "sale_price",
        "quantity",
    ]
    search_fields = ["id"]

    def get_product_display(self, obj):
        return obj.product_name

    get_product_display.short_description = "상품명"


class OrderPaymentAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "payment",
    )


admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(OrderPayment, OrderPaymentAdmin)
