from django.contrib import admin
from .models import Category, FoodItem

# Register your models here.

class categoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        "slug_name" : ("category_name",),
    }
    list_display = ("category_name", "restoran", "updated_date",) # ana sayfada liste durumudur
    search_fields = ("category_name", "restoran__vendor_name",) # arama alanı

class foodItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        "slug_name" : ("food_title",),
    }
    list_display = ("food_title", "category", "restoran", "price", "is_avail", "updated_date",) # ana sayfada liste durumudur
    search_fields = ("food_title", "category__category_name", "restoran__vendor_name","price",) # arama alanı
    list_filter = ("is_avail",)

admin.site.register(Category, categoryAdmin)
admin.site.register(FoodItem, foodItemAdmin)
