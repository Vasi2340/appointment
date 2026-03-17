from django.urls import path
from .views import toggle_payment

urlpatterns = [
    path(
        "toggle-payment/<int:appointment_id>/",
        toggle_payment,
        name="toggle_payment"
    )
]
