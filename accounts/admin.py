from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = [
        'user',
        'role',
        'is_blocked'
    ]

    list_filter = [
        'role',
        'is_blocked'
    ]

    search_fields = [
        'user__username',
        'user__email'
    ]