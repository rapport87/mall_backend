from django.urls import path
from .views import Products, ProductDetail

urlpatterns = [
    path("", Products.as_view(), name="products-list"),
    path("<int:pk>/", ProductDetail.as_view(), name="product-detail"),
]
