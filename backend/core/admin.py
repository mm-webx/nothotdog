from django.contrib import admin
from django.contrib.auth.models import User


@admin.register(User)
class UsersAdmin(admin.ModelAdmin):
    pass
