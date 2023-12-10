from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import UserForm
from .models import User
from django.contrib import messages
from django.contrib import auth
from django.urls import reverse
from . import utilities
from django.contrib.auth.decorators import login_required, user_passes_test

from django.core.exceptions import PermissionDenied

def check_vendor_user(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied

def check_custormer_user(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied


def register(request):
    if request.user.is_authenticated:
        messages.add_message(request, messages.INFO, "Zaten Giriş yaptığınız için dashboard yönlendirdim.")
        return redirect(reverse("accounts:decidemyboard"))
    form = UserForm()
    if request.method == "POST":
        print(request.POST)
        form = UserForm(request.POST)
        if form.is_valid():
            this_password = form.cleaned_data["password"] # bu cleaned_data çağrısında metho çağırır
            myuser = form.save(commit=False)
            myuser.set_password(this_password)
            myuser.role = User.CUSTOMER
            myuser.save()
            messages.add_message(request, messages.SUCCESS, "Kayıt işlemi başarıyla tamamlanmıştır.")
            return redirect("index")
        else:
            print("invalid form")
            print(form.errors)
    context = {
            "form" : form,
            }
    return render(request, "register.html", context= context)

def loginme(request):
    if request.user.is_authenticated:
        messages.add_message(request, messages.INFO, "Zaten Giriş yaptığınız için dashboard yönlendirdim.")
        return redirect(reverse("accounts:decidemyboard"))
    elif request.method == "POST":
        elmek = request.POST["email"]
        sifre = request.POST["password"]
        user = auth.authenticate(elmek = elmek, password = sifre) # bu süper bir şey resmen bana şifreli user gelir
        if user is not None:
            if not user.is_aktif:
                messages.add_message(request, messages.ERROR, "Hesabınız Pasiftir. Yöneticiye başvurunuz")
            else:    
                messages.add_message(request, messages.SUCCESS, "Başarı ile giriş yaptınız.")
                auth.login(request, user) # bir nevi requeste user ekliyor ve login oldum demek için diyor.
                return redirect(reverse("accounts:decidemyboard"))
        else:
            messages.add_message(request, messages.ERROR, "Parola veya elmek hatalıdır.")
    return render(request, "login.html")

def logout(request):
    auth.logout(request)
    messages.add_message(request, messages.INFO, "Başarı ile logout oldunuz.")
    return render(request, "logout.html")

@login_required(login_url= 'accounts:loginme')
def decidemyboard(request):
    gotohere = utilities.get_profil_redirect(request.user)
    if request.user.is_ustyonetici:
        return redirect(gotohere)
    else:
        return redirect(reverse(gotohere))

@login_required(login_url= 'accounts:loginme')
@user_passes_test(check_custormer_user)
def customboard(request):
    return render(request, 'dashboard.html')
    
@login_required(login_url= 'accounts:loginme')
@user_passes_test(check_vendor_user)
def vendorboard(request):
        return render(request, "vendorBoard.html")
    