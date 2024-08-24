from django.contrib import admin
from user.models import CustomUser
from django.utils import timezone
from datetime import timedelta
from import_export.admin import ImportExportModelAdmin

# Register your models here.
# from django.contrib.auth.admin import UserAdmin

# from .forms import CustomUserCreationForm, CustomUserChangeForm
# from .models import CustomUser

# class CustomUserAdmin(UserAdmin):
#     add_form = CustomUserCreationForm
#     form = CustomUserChangeForm

#     model = CustomUser

#     list_display = ('username', 'email', 'is_active',
#                     'is_staff', 'is_superuser', 'last_login',)
#     list_filter = ('is_active', 'is_staff', 'is_superuser')
#     fieldsets = (
#         (None, {'fields': ('username', 'email', 'password')}),
#         ('Permissions', {'fields': ('is_staff', 'is_active',
#          'is_superuser', 'groups', 'user_permissions')}),
#         ('Dates', {'fields': ('last_login', 'date_joined')})
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
#          ),
#     )
#     search_fields = ('email',)
#     ordering = ('email',)

# admin.site.register(CustomUser)
@admin.register(CustomUser)
class CustomUserModelAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display=('email', 'username', 'is_superuser', 'is_staff', 'is_new')
    list_filter=('last_login', 'is_active')

    def is_new(self,obj):
        return obj.date_joined >= timezone.now()-timedelta(days=30)
    is_new.boolean=True
