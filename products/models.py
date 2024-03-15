from django.db import models
from common.models import CommonModel
from categories.models import Category


class Product(CommonModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.PositiveIntegerField(default=0)
    sale_price = models.PositiveIntegerField(default=0)
    shipping_fee = models.PositiveIntegerField(default=0)
    thumbnail = models.URLField()
    categories = models.ManyToManyField(  # 필드명과 타입 변경
        Category,
        blank=True,
        related_name="products",
    )
    stock = models.PositiveIntegerField(default=0)
    DISPLAY_STATUS_CHOICES = [
        ("Y", "Y"),
        ("N", "N"),
    ]
    display_status = models.CharField(
        max_length=1, default="N", choices=DISPLAY_STATUS_CHOICES
    )
    # product_images = models.ManyToManyField(
    #     "products.ProductImage",
    #     related_name="products",
    # )
    detailed_description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class ProductImage(CommonModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
    )
    photo = models.URLField()

    def __str__(self):
        return f"Image for product {self.product.id}"
