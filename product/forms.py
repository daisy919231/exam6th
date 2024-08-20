from django import forms
from product.models import Product 
from django.contrib.auth.models import User

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','description', 'price', 'category', 'discount','quantity','slug']