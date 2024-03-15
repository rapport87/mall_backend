from django.db import models
from django.core.exceptions import ValidationError
from common.models import CommonModel
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel, CommonModel):
    name = models.CharField(max_length=255)
    parent = TreeForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="subcategories",
    )

    def clean(self):
        if self.parent == self:
            raise ValidationError("현재 카테고리를 상위 카테고리로 지정할 수 없습니다.")

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ["name"]
