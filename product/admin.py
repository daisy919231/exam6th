from django.contrib import admin
from django.utils import timezone
from datetime import timedelta
from product.models import Product, Category, Comment, Attribute, AttributeValue, Image
from import_export.admin import ImportExportModelAdmin

# Register your models here.
# admin.site.register(Product)
# admin.site.register(Category)
# admin.site.register(Comment)
# admin.site.register(Attribute)
# admin.site.register(AttributeValue)
# admin.site.register(Image)
# admin.site.register(ProductAttribute)



@admin.register(Product)
class ProductModelAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display=('name', 'description', 'price', 'quantity','is_new')
    list_filter=('quantity',)
    search_fields=['name', 'quantity']

    def is_new(self,obj):
        return obj.created_at >= timezone.now()-timedelta(days=30)
    is_new.boolean=True


@admin.register(Category)
class CategoryModelAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display=('title','is_new')
    
    

    def is_new(self,obj):
        return obj.created_at >= timezone.now()-timedelta(days=30)
    is_new.boolean=True


@admin.register(Comment)
class CommentModelAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display=('rating','is_new')
    
    

    def is_new(self,obj):
        return obj.created_at >= timezone.now()-timedelta(days=30)
    is_new.boolean=True


@admin.register(Attribute)
class AttributeModelAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display=('name','is_new')
   
    search_fields=['name']

    def is_new(self,obj):
        return obj.created_at >= timezone.now()-timedelta(days=30)
    is_new.boolean=True


@admin.register(AttributeValue)
class AttributeValueModelAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display=('value', 'attribute', 'is_new')
    list_filter=('product', )
    

    def is_new(self,obj):
        return obj.created_at >= timezone.now()-timedelta(days=30)
    is_new.boolean=True


@admin.register(Image)
class ImageModelAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display=('image', 'product', 'is_new')
    list_filter=('product', )
    

    def is_new(self,obj):
        return obj.created_at >= timezone.now()-timedelta(days=30)
    is_new.boolean=True
