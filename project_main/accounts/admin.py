from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from .models import User, UserProfile
from django.contrib.auth.admin import UserAdmin


class MyUserAdmin(UserAdmin):
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    add_fieldsets = (
        (
        "Giriş", {
            "classes" : ("wide",),
            "fields" : ("role", "isim", "soyisim", "elmek", "phone", "username","password1","password2")
        }
    ),
    )

    list_display = ("isim", "soyisim", "elmek", "role", "created_date", "son_login","is_aktif",)
    search_fields = ("isim", "kullanici_adi","joined_date","created_date")
    ordering = ("-created_date",)
    exclude = ("last_login",)
    
# Register your models here.
admin.site.register(User, MyUserAdmin)
admin.site.register(UserProfile)