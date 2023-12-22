from django.urls import path, include
from . import views

app_name = "accounts"

urlpatterns = [
    path('registerUser/', views.register, name="register"),
    path('login/', views.loginme, name="loginme"),
    path('logout/', views.logout, name="logoutme"),
    path('decideWheretoGo/', views.decidemyboard, name='decidemyboard'),
    path('musteriBoard/', views.customboard, name = "musterinDashboard"),
    path('vendorBoard/', views.vendorboard , name = "restoranDashboard"),
    path('activateme/<uid64>/<mytoken>/', views.activate, name= "activate"),
    path('forgotpassword/', views.forgotpassword, name= "forgotpassword"),
    path('resetme/<uid64>/<mytoken>/', views.resetme, name= "resetme"),
    path("reset_password/", views.reset_password, name = "reset_password")
]