# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    class MarketingAgreeChoices(models.TextChoices):
        YES = ("Y", "예")
        NO = ("N", "아니오")

    first_name = models.CharField(max_length=30, blank=True, editable=False)
    last_name = models.CharField(max_length=150, blank=True, editable=False)
    name = models.CharField(
        max_length=150,
        default="",
    )
    tel = models.CharField(max_length=255, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    marketing_agree_yn = models.CharField(
        max_length=1,
        choices=MarketingAgreeChoices.choices,
    )

    def __str__(self):
        return self.username


# @receiver(post_save, sender=User)
# def create_user_cart(sender, instance, created, **kwargs):
#     if created:
#         from carts.models import Cart
#         Cart.objects.create(user=instance)
