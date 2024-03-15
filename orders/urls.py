from django.urls import path
from .views import (
    OrderListView,
    OrderDetailView,
    UserOrdersView,
    UserOrderItemsView,
    CreateOrderView,
)

urlpatterns = [
    path("", OrderListView.as_view(), name="orders-list"),
    path("create/", CreateOrderView.as_view(), name="create-order"),
    path("<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
    path("<str:username>/", UserOrdersView.as_view(), name="user-orders"),
    path(
        "<str:username>/<int:pk>/",
        UserOrderItemsView.as_view(),
        name="user-order-items",
    ),
]
