from django import forms
from vendors.models import Vendor
from accounts.validators import file_extension_validation

class VendorForm(forms.ModelForm):
    # kendi alanlarımı override olarak ekleyebilirim.

    vendor_lisans = forms.FileField(widget = forms.FileInput(attrs={"class" : "btn btn-info",}), 
                                  validators = [file_extension_validation,])
    class Meta:
        model = Vendor
        fields = ["vendor_name", "vendor_lisans",]
        