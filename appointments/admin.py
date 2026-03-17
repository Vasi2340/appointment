from django.contrib import admin
from .models import Appointment, Note

# Register your models here.

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('client', 'psychologist', 'start_time','paid')
    list_filter = ('paid', 'psychologist')

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("client", "author", "visible_to_client", "created_at")