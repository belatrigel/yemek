from django.contrib import admin
from vendors.models import Vendor

# Register your models here.

class VendorAdmin(admin.ModelAdmin):
    filter_horizontal = ()
    list_filter = ["is_approved", "vendor_name",]
    fieldsets = ()
    
    list_display = ("vendor_name", "user", "is_approved", "created_at", "modified_at",)
    list_display_links = ["user","vendor_name",]
    search_fields = ("vendor_name", "is_approved", "created_at",)
    ordering = ("-created_at",)

admin.site.register(Vendor, VendorAdmin)