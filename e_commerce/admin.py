from django.contrib import admin
from django.utils import timezone
from datetime import timedelta
# Register your models here.
from .models import Customer
from django.contrib import admin
# admin.site.register(Customer)
from django.contrib.auth.models import User
from import_export.admin import ImportExportModelAdmin

@admin.register(Customer)
class CustomerModelAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display=('full_name','bill_address', 'phone_num','is_new')
    list_filter=('bill_address', 'created_at')
    search_fields=['first_name','last_name', 'phone_num']

    def is_new(self,obj):
        return obj.created_at >= timezone.now()-timedelta(days=30)
    is_new.boolean=True

