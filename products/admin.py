from django.contrib import admin
from .models import Product, ProductImage
from django import forms
from django.forms import CheckboxSelectMultiple


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        widgets = {
            "display_status": forms.RadioSelect(choices=Product.DISPLAY_STATUS_CHOICES),
            "categories": CheckboxSelectMultiple(),  # 다대다 필드를 위한 위젯
        }


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = [
        "name",
        "description",
        "price",
        "stock",
        "thumbnail",
        "display_categories",  # 다대다 관계를 표시하기 위한 메서드
        "sale_price",
        "display_status",
    ]
    list_filter = ["categories", "price"]  # 필터 수정
    search_fields = ["name", "categories__name"]

    def display_categories(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])

    display_categories.short_description = "Categories"


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ["product", "id"]
    search_fields = ["product__name"]
