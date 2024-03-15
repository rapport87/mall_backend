from django.db import models
import json
from common.models import CommonModel


class Order(CommonModel):
    user_id = models.IntegerField()
    username = models.CharField(max_length=255, verbose_name="주문자 성함")
    recipient_name = models.CharField(max_length=255, verbose_name="받는분 성함")
    recipient_tel = models.CharField(max_length=255, verbose_name="받는분 연락처")
    address = models.CharField(max_length=255, verbose_name="주소")
    address_detail = models.CharField(max_length=255, verbose_name="상세주소")
    zip_code = models.CharField(max_length=255, verbose_name="우편번호")
    order_request = models.TextField(verbose_name="요청사항")
    shipping_fee = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Order {self.id}"

    @property
    def total_price(self):
        return sum(item.quantity * item.sale_price for item in self.order_items.all())


class OrderItem(CommonModel):
    order = models.ForeignKey(
        Order, related_name="order_items", on_delete=models.CASCADE
    )
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=255, verbose_name="상품명")
    sale_price = models.PositiveIntegerField(default=0, verbose_name="판매가")
    quantity = models.PositiveIntegerField(default=1, verbose_name="개수")
    thumbnail = models.URLField()

    def __str__(self):
        return self.product_name


class OrderPayment(CommonModel):
    BANK_TRANSFER = 1
    CREDIT_CARD = 2
    SAMSUNG_PAY = 3

    PAYMENT_CHOICES = [
        (BANK_TRANSFER, "무통장입금"),
        (CREDIT_CARD, "신용카드"),
        (SAMSUNG_PAY, "삼성페이"),
    ]

    order = models.ForeignKey(
        Order, related_name="order_payment", on_delete=models.CASCADE
    )
    payment = models.IntegerField(choices=PAYMENT_CHOICES)

    def __str__(self):
        return self.get_payment_display()
