from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Appointment
from .forms import AppointmentForm


@login_required
def toggle_payment(request, appointment_id):

    appointment = get_object_or_404(Appointment, id=appointment_id)

    appointment.paid = not appointment.paid
    appointment.save()

    return redirect("client_detail", client_id=appointment.client.id)

@login_required
def create_appointment(request):

    if request.method == "POST":
        form = AppointmentForm(request.POST, psychologist=request.user)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.psychologist = request.user
            appointment.save()
            return redirect("psychologist_dashboard")
    else:
        form = AppointmentForm(psychologist=request.user)

    return render(request, "create_appointment.html", {"form": form})

@login_required
def cancel_appointment(request, appointment_id):

    appointment = get_object_or_404(Appointment, id=appointment_id)

    # allow only related users
    if request.user == appointment.client or request.user == appointment.psychologist:
        appointment.delete()

    return redirect("client_dashboard")