from django.contrib import admin
from product.models import Product, Category, Comment, Attribute, AttributeValue, Image

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Attribute)
admin.site.register(AttributeValue)
admin.site.register(Image)
# admin.site.register(ProductAttribute)