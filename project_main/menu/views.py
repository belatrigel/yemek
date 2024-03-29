from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from menu.forms import CategoryForm, FoodForm
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

@login_required(login_url= 'accounts:loginme')
@user_passes_test(check_vendor_user)
def add_food(request):
    if request.method == "POST":
        cat_form = FoodForm(request.POST, request.FILES) # imge veya pdf varsa o zaman bunu kullan.
        if cat_form.is_valid():
            food_title = cat_form.cleaned_data["food_title"] # fields alanındakilerden çek
            this_food = cat_form.save(commit=False) # vt ye yazma ama nesneyi al
            this_food.slug_name = slugify(food_title)
            this_food.restoran = get_object_or_404(Vendor, user= request.user)
            cat_form.save() # aslında yukarıdaki ile resmen category nesnesi bağ kurdum save diyince bunu kaydedecek
            messages.add_message(request, messages.SUCCESS, "Food başarıyla kayıt edilmiştir.")
            return redirect(reverse("menu:food_by_category", args=(this_food.category.pk,)))
        else:
            print(cat_form.errors)
    else:
        cat_form = FoodForm()
        # sadece o restorana ait kategoryler gelsin ki onlar seçilebilsin.
        cat_form.fields['category'].queryset = Category.objects.filter(restoran = get_object_or_404(Vendor, user= request.user))
    
    context = {
        "cat_form" : cat_form,
    }
    return render(request, "menu/add_food.html", context=context,)

@login_required(login_url= 'accounts:loginme')
@user_passes_test(check_vendor_user)
def edit_food(request, pk=None):
    food = get_object_or_404(FoodItem, pk = pk) # gelen pk ile food nesnesi çekelim
    if request.method == "POST":
        food_form = FoodForm(request.POST, request.FILES, instance=food) # POST ise o zaman gelen bilgileri mevcut food itema yaslayalım. bu arada imaj veya pdf varsa o zaman FILES da olmalıdır.
        if food_form.is_valid():
            food_name = food_form.cleaned_data["food_title"] # fields alanındakilerden çek
            this_food = food_form.save(commit=False) # vt ye yazma ama nesneyi al
            this_food.slug_name = slugify(food_name)
            this_food.restoran = get_object_or_404(Vendor, user= request.user)
            food_form.save() # aslında yukarıdaki ile resmen category nesnesi bağ kurdum save diyince bunu kaydedecek
            messages.add_message(request, messages.SUCCESS, f"Food Item {food_name} başarıyla update edilmiştir.")
            return redirect(reverse("menu:food_by_category", args=(this_food.category.pk,)))
        else:
            print(food_form.errors)
    else:
        food_form = FoodForm(instance=food) # GET ise o zaman git o food bilgilerini al karşı tarafa dolu gönder
        # sadece o restorana ait kategoryler gelsin ki onlar seçilebilsin.
        food_form.fields['category'].queryset = Category.objects.filter(restoran = get_object_or_404(Vendor, user= request.user))
    
    
    context = {
        "food_form" : food_form,
        "food" : food,
    }
    return render(request, "menu/edit_food.html", context=context,)

@login_required(login_url= 'accounts:loginme')
@user_passes_test(check_vendor_user)
def delete_food(request, pk=None):
    food = get_object_or_404(FoodItem, pk = pk) # gelen pk ile nesne çekelim
    food.delete() # resmen commit ederek siler
    messages.add_message(request, messages.SUCCESS, "Food Item başarıyla silinmiştir.")
    return redirect(reverse("menu:food_by_category", args=(food.category.pk,)))




