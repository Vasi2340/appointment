from django.contrib import admin
from .models import Appointment, Note

# Register your models here.

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('client', 'psychologist', 'start_time','paid')
    list_filter = ('paid', 'psychologist')

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("client", "author", "visible_to_client", "has_attachment", "created_at")

    def has_attachment(self, obj):
        if obj.attachment:
            return "Yes"
        return ""