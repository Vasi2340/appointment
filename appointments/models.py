from django.db import models
from django.conf import settings

# Create your models here.

class Appointment(models.Model):
    psychologist = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='appointments_as_psychologist',
        limit_choices_to={'role':'psychologist'}
    )
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='appointment_as_client',
        limit_choices_to={'role':'client'}
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.client.username} - {self.start_time}"

class Note(models.Model):
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notes'
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='written_notes'
    )

    text = models.TextField()

    visible_to_client = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note for {self.client.username} by {self.author.username}"