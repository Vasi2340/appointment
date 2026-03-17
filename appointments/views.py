from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Appointment


@login_required
def toggle_payment(request, appointment_id):

    appointment = get_object_or_404(Appointment, id=appointment_id)

    appointment.paid = not appointment.paid
    appointment.save()

    return redirect("client_detail", client_id=appointment.client.id)