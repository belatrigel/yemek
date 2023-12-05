from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.models import PermissionsMixin

# phone regular expression --- min 8 max 13 only numbers
def validate_phone_format(value):
    if not re.match(r'^\d{8,13}$', value):
        raise ValidationError('Telefon numarası sadece sayılardan oluşmalıdır (8-13 uzunluğunda).')


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, name, surname, gorev, telno, username, elmek, sifre=None):
        if not name:
            raise ValueError("isim bilgisi girilmelidir")
        if not surname:
            raise ValueError("soyisim bilgisi girilmelidir")
        if not username:
            raise ValueError("kullanıcı adı bilgisi girilmelidir")
        if not gorev:
            raise ValueError("role bilgisi girilmelidir")
        if not telno:
            raise ValueError("telefon bilgisi girilmelidir")
        if not name:
            raise ValueError("isim bilgisi girilmelidir")
        user = self.model(
            elmek = self.normalize_email(elmek),
            isim = name,
            soyisim = surname,
            username = username,
            phone = telno,
            role = gorev,
        )
        user.set_password(sifre)
        user.save(using = self._db)

        return user
    
    def create_superuser(self, isim, soyisim, role, username, elmek, phone, password):
        # Validate the phone number here
        if not phone.isdigit() or len(phone) > 13 or len(phone) < 8:
            raise ValueError('Telefon numarası sadece sayılardan oluşmalıdır (8-13 uzunluğunda).')

        user = self.create_user(
            elmek = self.normalize_email(elmek),
            name = isim,
            surname = soyisim,
            kullanici_adi= username,
            sifre = password,
            telno = phone,
            gorev = role,
            )
        user.is_yonetici = True
        user.is_aktif = True
        user.is_ustyonetici = True
        user.is_staff = True

        user.save(using=self._db)

        return user

class KisiAbsModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    joined_date  = models.DateTimeField(auto_now_add=True)
    son_login    = models.DateTimeField(auto_now=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class User(AbstractBaseUser, KisiAbsModel, PermissionsMixin):
    RESTAURANT = 1
    CUSTOMER = 2
    choices = (
        (RESTAURANT, "Vendor"),
        (CUSTOMER, "müşteri"),
    )
    role = models.PositiveSmallIntegerField(choices=choices, blank=True, null=True)
    isim = models.CharField(max_length=255, verbose_name="Adınız")
    soyisim = models.CharField(max_length=255, verbose_name="Soyisminiz")
    username = models.CharField(max_length=64, unique=True, verbose_name="Takma isminiz")
    elmek = models.EmailField(max_length=128, unique=True)
    phone = models.CharField(max_length=13, validators=[validate_phone_format])
    password = models.CharField(max_length=128, verbose_name= "sifre", null=True)

    is_yonetici = models.BooleanField(default=False)
    is_aktif = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_ustyonetici = models.BooleanField(default=False)

    REQUIRED_FIELDS = ["username", "isim", "soyisim", "phone", "role",]
    USERNAME_FIELD = "elmek"

    objects = UserManager()

    def __str__(self):
        return f"{self.isim.title()} {self.soyisim.title()}, {self.elmek.split('@')[0]}"

    def has_perm(self, perm, obj=None):
        return self.is_yonetici

    def has_module_perms(self, app_label):
        return True
    
class UserProfile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=False, verbose_name="Kişi")
    profile_pic = models.ImageField(upload_to="users/profile_pic", null=True, blank=True, verbose_name="Profil Resmi")
    cover_pic = models.ImageField(upload_to="users/cover_pic", null=True, blank=True, verbose_name="Kapak Resmi")
    adress_1 = models.CharField(max_length=100, null=True,blank=True, verbose_name="Adres Satırı 1")
    adress_2 = models.CharField(max_length=100, null=True,blank=True, verbose_name="Adres Satırı 2")
    country = models.CharField(max_length=100, null=True,blank=True, verbose_name="Ülke")
    state = models.CharField(max_length=100, null=True,blank=True, verbose_name="Eyalet")
    city = models.CharField(max_length=100, null=True,blank=True, verbose_name="Şehir")
    pin = models.CharField(max_length=100, null=True,blank=True, verbose_name="Pin Kodu")
    latitude = models.CharField(max_length=20, null=True,blank=True, verbose_name="Enlem")
    longitute = models.CharField(max_length=20, null=True,blank=True, verbose_name="Boylam")
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user}"



from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def profile_receiver_post(sender, created, instance , **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        print("user is created")
    else: # bu sefer user update oldu
        try:
            this_profile = UserProfile.objects.get(user=instance)
            this_profile.save()
            print("user is updated")
            # bu noktada user silersem direk profilden de siliniyor bu nesne.
        except:
            UserProfile.objects.create(user=instance)


# post_save.connect(receiver = profile_receiver_post, sender=User)
    
    
    

