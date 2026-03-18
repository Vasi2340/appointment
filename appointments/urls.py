from django.urls import path
from .views import toggle_payment
from .views import create_appointment, cancel_appointment

urlpatterns = [
    path(
        "toggle-payment/<int:appointment_id>/",
        toggle_payment,
        name="toggle_payment"
    ),
    path("create/", create_appointment, name="create_appointment"),
    path("cancel/<int:appointment_id>/", cancel_appointment, name="cancel_appointment"),
]
