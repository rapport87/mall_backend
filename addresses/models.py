from django.db import models
from common.models import CommonModel
from users.models import User


class Address(CommonModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    address_detail = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)

    def __str__(self):
        return self.address_name
