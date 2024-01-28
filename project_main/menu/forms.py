from django import forms
from menu.models import Category, FoodItem
from accounts.validators import file_extension_validation

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            "category_name",
            "description",
        ]

class FoodForm(forms.ModelForm):
    food_image = forms.FileField(widget = forms.FileInput(attrs={"class" : "btn btn-info w-100",}), 
                                  validators = [file_extension_validation,])
    class Meta:
        model = FoodItem
        fields = [
            "category",
            "food_title",
            "description",
            "price",
            "food_image",
            "is_avail",
        ]