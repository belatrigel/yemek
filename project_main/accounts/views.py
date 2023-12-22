from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import UserForm
from .models import User
from django.contrib import messages
from django.contrib import auth
from django.urls import reverse
from . import utilities
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator


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
            
            # send verifikasyon elmek helper fonksiyonu
            utilities.send_verificasyion_elmek(request, myuser,
                                               "Hello From FoodOnline, Please activate your account",
                                               "elmek/verifyme.html")

            messages.add_message(request, messages.SUCCESS, "Kayıt işlemi başarıyla tamamlanmıştır. Lütfen elmek adresinize gidip aktivasyon işleminizi tamamlayınız.")
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

def activate(request, uid64, mytoken):
    try:
        pk = urlsafe_base64_decode(uid64).decode()
        user = User.objects.get(pk = pk)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user,mytoken):
        user.is_aktif = True
        user.save()
        messages.add_message(request, messages.SUCCESS, "Aktivasyon Başarılıdır")
        return redirect(reverse("accounts:decidemyboard"))
    else:
        messages.add_message(request, messages.ERROR, "Aktivasyon Linki Bozuk!")
        return redirect("index")

def forgotpassword(request):
    if request.method == "POST":
        elmek2check = request.POST["email"]
        myuser = User.objects.filter(elmek__iexact = elmek2check)
        if myuser: # gerçekten böyle bir elmek adresli kayıt varsa
            myuser = User.objects.get(elmek = elmek2check)
            # elmek gönder, success mesajı ile birlikte index sayfasına gönder.
            utilities.send_verificasyion_elmek(request, myuser,
                                               "Hello From FoodOnline, Please Reset your account",
                                               "elmek/resetme.html")
            messages.add_message(request, messages.SUCCESS, "Lütfen elmek adresinize gidip resetleme işleminizi tamamlayınız.")
            return redirect("index")
        else:
             messages.add_message(request, messages.ERROR, "Böyle bir elmek sistemde kayıtlı değil. Lütfen Çek ediniz.")
    return render(request, "forgotpassword.html")

def resetme(request, uid64, mytoken):
    try:
        pk = urlsafe_base64_decode(uid64).decode()
        user = User.objects.get(pk = pk)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user,mytoken):
        request.session["uid"] = pk # bunu user seçip pk ile resetleme için kullanacağım.
        messages.add_message(request, messages.INFO, "Lütfen Yeni Şifrenizi Giriniz.")
        return redirect(reverse("accounts:reset_password"))
    else:
        messages.add_message(request, messages.ERROR, "Aktivasyon Linki Bozuk!")
        return redirect("index")
    
def reset_password(request):
    if request.method == "POST":
        password = request.POST["password"]
        repassword = request.POST["password1"]
        if password == repassword:
            user = User.objects.get(pk=request.session["uid"])
            user.set_password(password)
            user.is_aktif = True
            user.save()
            messages.add_message(request, messages.SUCCESS, "Şifreniz Değiştirildi. Lütfen Giriş Yapınız.")
            return redirect(reverse("accounts:loginme"))
        else:
            messages.add_message(request, messages.ERROR, "Farklı şifreler girdiniz. Eşitlik olmalıdır.")
    return render(request, "password_reset.html")