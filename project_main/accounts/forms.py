from django import forms
from .models import User

class UserForm(forms.ModelForm):
    # kendi alanlarımı override olarak ekleyebilirim.
    password  = forms.CharField(widget=forms.PasswordInput())
    validation_pass = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ["isim", "soyisim","username","elmek","phone", "password",]

    def clean(self):
        cleaned_data = super(UserForm,self).clean()
        sifre = cleaned_data["password"]
        validsifre = cleaned_data["validation_pass"]

        if sifre != validsifre:
            raise forms.ValidationError(
                "Sifre ve Tekrarı aynı değildir. Lütfen aynı sifreyi giriniz..."
            )