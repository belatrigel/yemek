from django.db import models
from vendors.models import Vendor

# Create your models here.

# menu kategorisi yani bir restoranın menu kategorisi vardır fast food gibi sea food gibi

class Category(models.Model):
    restoran = models.ForeignKey(Vendor, on_delete = models.CASCADE) # restoran silinirse bu kategori satırı da kople silinir
    category_name = models.CharField(max_length = 30, unique= True)
    slug_name = models.SlugField(max_length = 30, unique = True) # bunu kategori için urlde kullanacağım
    description = models.TextField(max_length = 300, blank = True)
    created_date = models.DateTimeField(auto_now_add = True) # bir kere ekle ve readonly ol
    updated_date = models.DateTimeField(auto_now = True) # her update sonrası şimdiyi kaydet

    def __str__(self):
        return f"{self.category_name}"
    
    class Meta:
        verbose_name = "katogori"
        verbose_name_plural = "kategoriler"

    def clean(self):
        self.category_name = self.category_name.lower()
    
class FoodItem(models.Model):
    restoran = models.ForeignKey(Vendor, on_delete = models.CASCADE) # restoran silinirse bu kategori satırı da kople silinir
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    food_title = models.CharField(max_length = 50, unique= True)
    slug_name = models.SlugField(max_length = 50, unique = True) # bunu kategori için urlde kullanacağım
    description = models.TextField(max_length = 300, blank = True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    food_image = models.ImageField(upload_to="food_items")
    is_avail = models.BooleanField(default = True)
    created_date = models.DateTimeField(auto_now_add = True) # bir kere ekle ve readonly ol
    updated_date = models.DateTimeField(auto_now = True) # her update sonrası şimdiyi kaydet

    def __str__(self):
        return f"{self.food_title}"
    



    
    
   



