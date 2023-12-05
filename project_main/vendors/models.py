from django.db import models
from accounts.models import User, UserProfile

# Create your models here.

class Vendor(models.Model):
    user = models.OneToOneField(User, related_name="vendor", on_delete= models.CASCADE)
    user_profile =  models.OneToOneField(UserProfile, related_name="restorant", on_delete= models.CASCADE)
    vendor_name = models.CharField(max_length=200, blank=False, unique=True)
    vendor_lisans = models.ImageField(upload_to="vendors/licence")
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.vendor_name}"
