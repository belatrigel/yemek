from django import forms
from .models import User, UserProfile

class UserForm(forms.ModelForm):
    # kendi alanlarımı override olarak ekleyebilirim.
    password  = forms.CharField(widget=forms.PasswordInput())
    validation_pass = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ["isim", "soyisim","username","elmek","phone", "password",]
        widgets = {
            'isim': forms.TextInput(attrs={'id': 'my-field-id'})
        }

    def clean(self):
        cleaned_data = super(UserForm,self).clean()
        sifre = cleaned_data["password"]
        validsifre = cleaned_data["validation_pass"]

        if sifre != validsifre:
            raise forms.ValidationError(
                "Sifre ve Tekrarı aynı değildir. Lütfen aynı sifreyi giriniz..."
            )

from accounts.validators import file_extension_validation

class UserProfileFrom(forms.ModelForm):
    profile_pic = forms.FileField(widget = forms.FileInput(attrs={"class" : "btn btn-info",}), 
                                  validators = [file_extension_validation,])
    cover_pic = forms.FileField(widget = forms.FileInput(attrs={"class" : "btn btn-info",}), 
                                  validators = [file_extension_validation,])
    
    adress = forms.CharField(widget = forms.TextInput(attrs={"required" : "required",
                                                             "placeholder" : "lütfen yazın...", }))

    class Meta:
        model = UserProfile
        fields = ["profile_pic", "cover_pic", "adress", "country",
                  "state", "city", "pin", "latitude", "longitute", ]
        
    def __init__(self, *args, **kargs):
        super(UserProfileFrom, self).__init__(*args,**kargs)
        for field in self.fields:
            if field=="latitude" or field=="longitute":
                self.fields[field].widget.attrs["readonly"] = "readonly"
                self.fields[field].widget.attrs["class"] = "btn-info"

    #latitude = forms.CharField(widget = forms.TextInput(attrs={"readonly" : "readonly",}))
    #longitute = forms.CharField(widget = forms.TextInput(attrs={"readonly" : "readonly",}))

