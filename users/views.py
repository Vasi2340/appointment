from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from appointments.models import Appointment
from django.utils import timezone

# Create your views here.

@login_required
def home(request):
    if request.user.role == 'psychologist':
        return redirect('psychologist_dashboard')
    elif request.user.role == 'client':
        return redirect('client_dashboard')
    
    return render(request, 'home.html')

@login_required
def psychologist_dashboard(request):
    appointments = Appointment.objects.filter(psychologist=request.user).order_by('start_time')

    next_appointment = appointments.filter(
        start_time__gte=timezone.now()
    ).order_by('start_time').first()
    return render(request, 'psychologist_dashboard.html', {
        'appointments': appointments,
        'next_appointment': next_appointment
    })

@login_required
def client_dashboard(request):
    appointments = Appointment.objects.filter(client=request.user).order_by('start_time')

    next_appointment = appointments.filter(
        start_time__gte=timezone.now()
    ).order_by('start_time').first()

    unpaid_appointments = appointments.filter(paid=False)
    total_due = sum(a.price for a in unpaid_appointments)

    return render(request, 'client_dashboard.html', {
        'appointments': appointments,
        'next_appointment': next_appointment,
        'total_due': total_due
    })
