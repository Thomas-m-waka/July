from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.db import models

from .models import withoutvehicle, withvehicle

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

class  withoutvehicleAdmin(admin.ModelAdmin):
    list_display = ("id", "id_number", "name", "phone_number", "company", "purpose", "time_in", "time_out", "today")
    list_filter = ['today']
    readonly_fields = ['time_in', 'time_out']

    # Register thumbnail for idphoto


class withvehicleAdmin(admin.ModelAdmin):
    list_display = ("id", "id_number", "name", "phone_number", "company", "purpose", "time_in", "time_out", "today")
    list_filter = ['today']
    readonly_fields = ['time_in', 'time_out']

    # Register thumbnails for idphoto and vehiclephoto


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

admin.site.register( withoutvehicle,  withoutvehicleAdmin)
admin.site.register(withvehicle, withvehicleAdmin)


