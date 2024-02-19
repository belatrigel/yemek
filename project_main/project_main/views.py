from django.http import HttpResponse
from django.shortcuts import render

from vendors.models import Vendor

def home(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_aktif=True)[:8]
    # böylece mesela top 8 restoran gidecektir.
    context = {
        "vendors" : vendors,
    }
    return render(request, "home.html", context=context)