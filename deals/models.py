from django.db import models
from products.models import Product
from common.models import CommonModel


class Deal(CommonModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"Deal {self.id}"
