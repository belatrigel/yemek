from django.shortcuts import render
from django.shortcuts import HttpResponse
from vendors.models import Vendor
from django.shortcuts import get_object_or_404
from menu.models import Category, FoodItem

# Create your views here.

def marketplace(request):
    vendors = Vendor.objects.filter(user__is_aktif = True, is_approved = True)
    sayac = vendors.count()
    context = {
        "restoranlar" : vendors,
        "sayac" : sayac,
    } 
    return render(request, "marketplace/listings.html", context=context)

from django.db.models import Prefetch

def vendor_menu_detail(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug = vendor_slug)
    categories = Category.objects.filter(restoran = vendor).prefetch_related(
        Prefetch(
            "fooditems",
            queryset= FoodItem.objects.filter(is_avail = True)
        )
    )
    context = {
        "vendor" : vendor,
        "categories" : categories,
    }
    return render(request, 'marketplace/menu_details.html', context=context,)