from django.contrib import admin
from .models import User
from .models import ClientProfile

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_staff')
    list_filter = ('role', 'is_staff')
    search_fields = ('username', 'email')

@admin.register(ClientProfile)
class CliemtProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'psychologist')