from django import forms
from .models import Note, Appointment
from users.models import ClientProfile

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

        def __init__(self, *args, **kwargs):
            psychologist = kwargs.pop("psychologist", None)
            self.psychologist = psychologist
            super().__init__(*args, **kwargs)

            if psychologist:
                client_ids = ClientProfile.objects.filter(
                    psychologist=psychologist
                ).values_list("user_id", flat=True)

                self.fields["client"].queryset = self.fields["client"].queryset.filter(id__in=client_ids)
        
        def clean(self):
            cleaned_data = super().clean()
            start_time = cleaned_data.get("start_time")
            client = cleaned_data.get("client")

            if start_time and client:

                # same psychologist + same time
                if Appointment.objects.filter(
                    psychologist=self.psychologist,
                    start_time=start_time
                ).exists():
                    raise forms.ValidationError("This time slot is already taken.")
                
                if Appointment.objects.filter(
                    client=client,
                    start_time=start_time
                ).exists():
                    raise forms.ValidationError("Client already has an appointment at this time.")

            return cleaned_data