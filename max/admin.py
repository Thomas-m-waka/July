from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.db import models

from .models import withoutvehicle, withvehicle
from easy_thumbnails.exceptions import InvalidImageFormatError
from easy_thumbnails.files import get_thumbnailer
# admin.py
from django.utils.html import format_html

def image_thumbnail(image_url):
    return format_html('<img src="{}" height="50"/>', image_url)

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

class WithoutVehicleAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "id_number", "phone_number", "company", "purpose", "time_in", "time_out","time_spent", "today", "idphoto_thumbnail", "Exit")
    list_filter = ['today']
    readonly_fields = ['time_in', 'time_out']



    def idphoto_thumbnail(self, obj):
        return format_html('<img src="{}" height="50"/>', obj.idphoto.url)
    idphoto_thumbnail.short_description = 'ID Photo'



class WithVehicleAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "id_number", "phone_number", "vehicle_registration", "company", "purpose", "time_in", "time_out","time_spent", "today", "idphoto_thumbnail", "vehiclephoto_thumbnail", "Exit")
    list_filter = ['today']
    readonly_fields = ['time_in', 'time_out']

    def idphoto_thumbnail(self, obj):
        return format_html('<img src="{}" height="50"/>', obj.idphoto.url)
    idphoto_thumbnail.short_description = 'ID Photo'

    def vehiclephoto_thumbnail(self, obj):
        return format_html('<img src="{}" height="50"/>', obj.vehiclephoto.url)
    vehiclephoto_thumbnail.short_description = 'Vehicle Photo'


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(withoutvehicle, WithoutVehicleAdmin)
admin.site.register(withvehicle, WithVehicleAdmin)


