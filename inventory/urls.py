from django.urls import path
from .views import (
    ReserveInventoryAPI,
    ConfirmCheckoutAPI,
    CancelCheckoutAPI,
    InventoryStatusAPI
)

urlpatterns = [
    path('inventory/reserve', ReserveInventoryAPI.as_view()),
    path('checkout/confirm', ConfirmCheckoutAPI.as_view()),
    path('checkout/cancel', CancelCheckoutAPI.as_view()),
    path('inventory/<str:sku>', InventoryStatusAPI.as_view()),
]
