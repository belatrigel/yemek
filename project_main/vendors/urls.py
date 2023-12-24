from django.urls import path, include
from . import views
from accounts.views import vendorboard

app_name = "vendors"

urlpatterns = [
    path("", vendorboard , name = "vendorDashboard"),
    path('registerVendor/', views.register, name="register"),
    path ("profile/", views.profile, name="vendor_profile"),
]