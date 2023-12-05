from django import forms
from vendors.models import Vendor

class VendorForm(forms.ModelForm):
    # kendi alanlarımı override olarak ekleyebilirim.
    class Meta:
        model = Vendor
        fields = ["vendor_name", "vendor_lisans",]
        