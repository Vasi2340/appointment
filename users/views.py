from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from appointments.models import Appointment, Note
from django.utils import timezone
from users.models import ClientProfile, User
from django.shortcuts import get_object_or_404
from appointments.forms import NoteForm, ClientNoteForm

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
    appointments = Appointment.objects.filter(
        psychologist=request.user
    ).order_by('start_time')

    clients = ClientProfile.objects.filter(
        psychologist=request.user
    )

    next_appointment = appointments.filter(
        start_time__gte=timezone.now()
    ).order_by('start_time').first()
    return render(request, 'psychologist_dashboard.html', {
        'appointments': appointments,
        'next_appointment': next_appointment,
        'clients': clients
    })

@login_required
def client_dashboard(request):
    appointments = Appointment.objects.filter(client=request.user).order_by('start_time')

    next_appointment = appointments.filter(
        start_time__gte=timezone.now()
    ).order_by('start_time').first()

    unpaid_appointments = appointments.filter(paid=False)
    total_due = sum(a.price for a in unpaid_appointments)

    notes = Note.objects.filter(
        client=request.user,
        visible_to_client=True
    ).order_by('-created_at')

    if request.method == "POST":
        form = ClientNoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.client = request.user
            note.author = request.user
            note.visible_to_client = True
            note.save()
            return redirect("client_dashboard")
    else:
        form = ClientNoteForm()

    return render(request, 'client_dashboard.html', {
        'appointments': appointments,
        'next_appointment': next_appointment,
        'total_due': total_due,
        'notes': notes,
        'form': form
    })

@login_required
def client_detail(request, client_id):

    client = get_object_or_404(User, id=client_id, role='client')

    appointments = Appointment.objects.filter(
        client=client
    ).order_by('start_time')

    unpaid_appointments = appointments.filter(paid=False)
    total_due = sum(a.price for a in unpaid_appointments)

    notes = Note.objects.filter(client=client).order_by('-created_at')

    if request.method == "POST":
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.client = client
            note.author = request.user
            note.save()
            return redirect("client_detail", client_id=client.id)
    else:
        form = NoteForm()

    return render(request, "client_detail.html", {
        "client": client,
        "appointments": appointments,
        "total_due": total_due,
        "notes": notes,
        "form": form
    })