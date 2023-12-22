from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings


def get_profil_redirect(user):
    if user.is_ustyonetici:
        myurl = "/admin"
    elif user.role == 1:
        myurl = "accounts:restoranDashboard"
    elif user.role == 2:
        myurl = "accounts:musterinDashboard"
    return myurl 

def send_verificasyion_elmek(request,user, elmek_subject, html_file):
    from_email = settings.DEFAULT_FROM_EMAIL
    mysite = get_current_site(request) # link için ilk domain demektir. www.xxx.com gibi çünkü request buraya gidecek
    # mesaj body kısmı aşağıda. user context kullanımı için, domain url oluşturmak için
    # token o kişiye bir kerelik toke oluşturmak için, uid ise url içindir
    # templates/ içinde elmek içinde html render edilecek ama zaten direk buradan gittiği için render_string
    message = render_to_string(html_file, {
        "user" : user,
        "domain" : mysite,
        "uid" : urlsafe_base64_encode(force_bytes(user.pk)),
        "token" : default_token_generator.make_token(user),
    })
    
    # aslında burada context olarak gidiyor tüm herşey
    to_email = user.elmek
    mail = EmailMessage(elmek_subject, message, from_email=from_email, to=[to_email,])
    mail.send()