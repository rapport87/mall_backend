from django.db import models
from users.models import User
from common.models import CommonModel


class Coupon(CommonModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Coupon {self.id}"
