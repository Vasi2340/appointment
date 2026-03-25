from django import forms
from .models import Note, Appointment
from users.models import ClientProfile
from datetime import timedelta

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["text", "attachment", "visible_to_client"]

class ClientNoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["text", "attachment"]


class AppointmentForm(forms.ModelForm):

    start_time = forms.DateTimeField(
        input_formats=["%Y-%m-%dT%H:%M"],
        widget=forms.DateTimeInput(
            attrs={
                "type": "datetime-local",
                "class": "form-control"
            }
        )
    )
    

    class Meta:
        model = Appointment
        fields = ["client", "start_time", "duration", "price"]

    def __init__(self, *args, **kwargs):
        psychologist = kwargs.pop("psychologist", None)
        super().__init__(*args, **kwargs)

        self.psychologist = psychologist
        self.fields["client"].widget.attrs.update({"class": "form-control"})
        self.fields["price"].widget.attrs.update({"class": "form-control"})
        self.fields["duration"].widget.attrs.update({"class": "form-control"})

        if psychologist:
            client_ids = ClientProfile.objects.filter(
                psychologist=psychologist
            ).values_list("user_id", flat=True)

            self.fields["client"].queryset = self.fields["client"].queryset.filter(id__in=client_ids)
        
    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        client = cleaned_data.get("client")
        end_time = start_time + timedelta(minutes=int(cleaned_data.get("duration", 60)))

        conflicts = Appointment.objects.filter(
            psychologist=self.psychologist,
            start_time__lt=end_time
        ).filter(
            start_time__lt=end_time
        )

        for appt in conflicts:
            appt_end = appt.start_time + timedelta(minutes=appt.duration)
            if start_time < appt_end:
                raise forms.ValidationError("This appointment overlaps with another.")

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