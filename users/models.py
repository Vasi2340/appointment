from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('psychologist', 'Psychologist'),
        ('client', 'Client'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_profile')
    psychologist = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='clients',
        limit_choices_to={'role':'psychologist'}
    )

    def __str__(self):
        return f"{self.user.username} -> {self.psychologist.username}"