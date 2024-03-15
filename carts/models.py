from django.db import models
from users.models import User
from products.models import Product
from common.models import CommonModel


class Cart(CommonModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="cart",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="cart",
    )
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Cart {self.id}"
