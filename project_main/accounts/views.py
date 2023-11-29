from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import UserForm
from .models import User
from django.contrib import messages

def register(request):
    form = UserForm()
    if request.method == "POST":
        print(request.POST)
        form = UserForm(request.POST)
        if form.is_valid():
            this_password = form.cleaned_data["password"]
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
