from django.db import models
from accounts.models import User, UserProfile
from accounts import utilities

# Create your models here.

class Vendor(models.Model):
    user = models.OneToOneField(User, related_name="vendor", on_delete= models.CASCADE)
    user_profile =  models.OneToOneField(UserProfile, related_name="restorant", on_delete= models.CASCADE)
    vendor_name = models.CharField(max_length=200, blank=False, unique=True)
    vendor_lisans = models.ImageField(upload_to="vendors/licence")
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    vendor_slug = models.SlugField(max_length = 100, unique=True,)

    def __str__(self):
        return f"{self.vendor_name}"
    
    def save(self, *args, **kwargs):
        if self.pk is not None: # yani daha önce oluşmuş bir vendor, ilk save değil yani
            ilkHali = Vendor.objects.get(pk = self.pk)
            if ilkHali.is_approved != self.is_approved: # daha save edilmediği için vtdeki ile karşılaştır
                elmek_template = "elmek/vendor_approval.html"
                context = {
                    "user" : self.user,
                    "decision" : self.is_approved,
                }
                if self.is_approved is True:
                    elmek_subject = "Tebrikler! Admin tarafından sistemden onay verilmiştir."
                else:
                    elmek_subject = "Üzgünüz! Bu sitede satış yapabilmeniz için yeterli seviyede değilsiniz."

                utilities.send_decision_elmek(elmek_subject, elmek_template, context)
        return super(Vendor, self).save(*args, **kwargs)
