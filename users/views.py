from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

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
    return render(request, 'psychologist_dashboard.html')

@login_required
def client_dashboard(request):
    return render(request, 'client_dashboard.html')
