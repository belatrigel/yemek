from django.urls import path, include
from . import views

app_name = "vendors"

urlpatterns = [
    path('registerVendor/', views.register, name="register"),
]