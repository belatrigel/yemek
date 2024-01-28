from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse

from .forms import VendorForm
from accounts.forms import UserProfileFrom

from django.shortcuts import get_object_or_404

from accounts.forms import UserForm
from vendors.models import Vendor
from vendors.forms import VendorForm
from accounts.models import User, UserProfile
from django.contrib import messages
from accounts import utilities

# Create your views here.

def register(request):
    if request.user.is_authenticated:
        messages.add_message(request, messages.INFO, "Zaten Giriş yaptığınız için dashboard yönlendirdim.")
        return redirect(reverse("accounts:dashboardme"))
    form = UserForm()
    v_form = VendorForm()

    if request.method == "POST":
        # formlar htmlde bağlanmıştı. buna göre POST ile alabilirim.
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES) # bir binary dosya gönderirsem mutlaka files ile al 

        if form.is_valid() and v_form.is_valid(): # is_valid dersem clean() çalışıp cleaned data elde edilir.
            name = form.cleaned_data["isim"]
            sname = form.cleaned_data["soyisim"]
            takmai = form.cleaned_data["username"]
            elmek = form.cleaned_data["elmek"]
            tel = form.cleaned_data["phone"]
            sifre = form.cleaned_data["password"]
            kisi = User.objects.create_user(name = name, surname = sname, 
                                            gorev = User.RESTAURANT, username = takmai, 
                                            elmek = elmek, telno = tel, 
                                            sifre = sifre)

            kisi.save()

            vendor = v_form.save(commit=False) # v_form içinde 2 alan zaten var.
            vendor.user = kisi
            vendor.user_profile = UserProfile.objects.get(user = kisi) # ben kisi save dediğim anda signals sayesinde profile otomatik oluştu ve bağlandı

            vendor.save()

            # send verifikasyon elmek helper fonksiyonu tıpkı normal user sign up gibi...
            utilities.send_verificasyion_elmek(request, kisi,
                                               "Hello From FoodOnline, Please activate your account",
                                               "elmek/verifyme.html")

            messages.add_message(request, messages.SUCCESS, "Restoran Kayıt işlemi başarıyla tamamlanmıştır. Onay bekleyiniz.")
            return redirect("index")

        else:
            print("invalid forms")
            print(form.errors)
            print(v_form.errors)

    context = {
        "form" : form,
        "v_form" : v_form,
    }
    return render(request, "registerVendor.html", context= context)

from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_vendor_user

@login_required(login_url= 'accounts:loginme')
@user_passes_test(check_vendor_user)
def profile(request):

    thisvendor = get_object_or_404(Vendor, user=request.user)
    thisprofile = get_object_or_404(UserProfile, user= request.user)

    v_form = VendorForm(instance=thisvendor)
    up_form = UserProfileFrom(instance=thisprofile)

    if request.method == "POST" : # submit butona bastım

        v_form = VendorForm(request.POST, request.FILES, instance=thisvendor)
        up_form = UserProfileFrom(request.POST, request.FILES, instance=thisprofile)

        if v_form.is_valid() and up_form.is_valid():
            v_form.save()
            up_form.save()
            messages.add_message(request, messages.SUCCESS, "Profil güncelleme başarılı şekilde tamamlandı")
            return redirect(reverse("vendors:vendor_profile"))
        else:
            print(v_form.errors)
            print(up_form.errors)

    context = {
        "vendor_profile_form" : v_form,
        "user_profile_form" : up_form,
        "profile" : thisprofile,
        "vendor" : thisvendor,
    }

    return render(request,"vendor_profile.html", context = context,)