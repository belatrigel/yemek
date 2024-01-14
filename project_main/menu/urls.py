from django.urls import path, include
from . import views

app_name = "menu"

urlpatterns = [
    path("menu-builder/",views.menu_builder, name="menu-builder"),
    path("category/<int:pk>/",views.food_by_category, name="food_by_category"),
    path("add_category/", views.add_category, name="add_category"),
    path("edit_category/<int:pk>/",views.edit_category, name="edit_category"),
    path("delete_category/<int:pk>/",views.delete_category, name="delete_category"),


]