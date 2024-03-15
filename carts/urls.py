from django.urls import path
from .views import Carts

urlpatterns = [
    path("", Carts.as_view()),
    path("<int:pk>/", Carts.as_view()),
]
