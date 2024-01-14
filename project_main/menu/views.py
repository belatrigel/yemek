from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from menu.forms import CategoryForm
from vendors.models import Vendor
from menu.models import Category, FoodItem
from django.template.defaultfilters import slugify

from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_vendor_user

from django.contrib import messages

# Create your views here.
@login_required(login_url= 'accounts:loginme')
@user_passes_test(check_vendor_user)
def menu_builder(request):
    vendor = get_object_or_404(Vendor, user= request.user)
    categories = Category.objects.filter(restoran = vendor).order_by("created_date")
    context = {
        "kategoriler" : categories,
    }
    return render(request, "menu/menu_builder.html", context=context)



@login_required(login_url= 'accounts:loginme')
@user_passes_test(check_vendor_user)
def food_by_category(request, pk=None):
    vendor = get_object_or_404(Vendor, user= request.user)
    category = get_object_or_404(Category, pk=pk)
    fooditems = FoodItem.objects.filter(restoran=vendor, category=category)
    context = {
        "items" : fooditems,
        "category_name" : category.category_name,
    }
    return render(request, "menu/food_by_category.html", context = context,)



@login_required(login_url= 'accounts:loginme')
@user_passes_test(check_vendor_user)
def edit_category(request, pk=None):
    category = get_object_or_404(Category, pk = pk) # gelen pk ile nesne çekelim
    if request.method == "POST":
        cat_form = CategoryForm(request.POST, instance=category) # POST ise o zaman gelen bilgileri mevcut categorye yaslayalım.
        if cat_form.is_valid():
            category_name = cat_form.cleaned_data["category_name"] # fields alanındakilerden çek
            this_category = cat_form.save(commit=False) # vt ye yazma ama nesneyi al
            this_category.slug_name = slugify(category_name)
            this_category.restoran = get_object_or_404(Vendor, user= request.user)
            cat_form.save() # aslında yukarıdaki ile resmen category nesnesi bağ kurdum save diyince bunu kaydedecek
            messages.add_message(request, messages.SUCCESS, "Kategori başarıyla update edilmiştir.")
            return redirect(reverse("menu:menu-builder"))
        else:
            print(cat_form.errors)
    else:
        cat_form = CategoryForm(instance=category) # GET ise o zaman git o kategori bilgilerini al karşı tarafa dolu gönder
    
    context = {
        "cat_form" : cat_form,
        "category" : category,
    }
    return render(request, "menu/edit_category.html", context=context,)



@login_required(login_url= 'accounts:loginme')
@user_passes_test(check_vendor_user)
def delete_category(request, pk=None):
    category = get_object_or_404(Category, pk = pk) # gelen pk ile nesne çekelim
    category.delete() # resmen commit ederek siler
    messages.add_message(request, messages.SUCCESS, "Kategori başarıyla silinmiştir.")
    return redirect(reverse("menu:menu-builder"))



@login_required(login_url= 'accounts:loginme')
@user_passes_test(check_vendor_user)
def add_category(request):
    if request.method == "POST":
        cat_form = CategoryForm(request.POST)
        if cat_form.is_valid():
            category_name = cat_form.cleaned_data["category_name"] # fields alanındakilerden çek
            this_category = cat_form.save(commit=False) # vt ye yazma ama nesneyi al
            this_category.slug_name = slugify(category_name)
            this_category.restoran = get_object_or_404(Vendor, user= request.user)
            cat_form.save() # aslında yukarıdaki ile resmen category nesnesi bağ kurdum save diyince bunu kaydedecek
            messages.add_message(request, messages.SUCCESS, "Kategori başarıyla kayıt edilmiştir.")
            return redirect(reverse("menu:menu-builder"))
        else:
            print(cat_form.errors)
    else:
        cat_form = CategoryForm()
    
    context = {
        "cat_form" : cat_form,
    }
    return render(request, "menu/add_category.html", context= context)