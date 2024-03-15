from django.urls import path
from .views import CategoryProductsView

urlpatterns = [
    path(
        "<int:categories_id>/", CategoryProductsView.as_view(), name="category-products"
    ),
]
