from django import forms
from .models import Note, Appointment

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["text", "attachment", "visible_to_client"]

class ClientNoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["text", "attachment"]

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["client", "start_time", "price"]