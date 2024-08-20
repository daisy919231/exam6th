from django.db import models
from user.models import CustomUser
from django.utils.text import slugify

# Create your models here.
class BaseModel(models.Model):
    created_at=models.DateTimeField(null=True, blank=True, auto_now_add=True)
    updated_at=models.DateTimeField(null=True, blank=True, auto_now=True)

    class Meta:
        abstract=True

class Category(BaseModel):
    title=models.CharField(max_length=255, null=True, blank=True, unique=True)
    slug=models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug=slugify(self.title)
        super(Category,self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural='Categories'

class Product(BaseModel):

    name=models.CharField(null=True, blank=True, max_length=100)
    description=models.TextField(null=True, blank=True)
    price=models.FloatField(null=True, blank=True)
    category=models.ForeignKey(Category, on_delete=models.CASCADE,  related_name='products')
    discount=models.PositiveIntegerField(default=0, null=True, blank=True)
    quantity=models.PositiveIntegerField(default=0)
    slug=models.SlugField(null=True, blank=True)


    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug=slugify(self.name)
        super(Product,self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    @property
    def discounted_price(self):
        if self.discount > 0:
            return int(self.price * (1-self.discount/100))
        return self.price



class Image(BaseModel):
    image=models.ImageField(upload_to='products/', null=True, blank=True)
    product=models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    is_primary=models.BooleanField(default=False)


class Comment(BaseModel):
    class RatingChoices(models.IntegerChoices):
        zero=0
        one=1
        two=2
        three=3
        four=4
        five=5
    message=models.TextField(null=True, blank=True)
    file=models.FileField(upload_to='comments/', null=True, blank=True )
    product=models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE, related_name='custom_comments')
    rating=models.PositiveIntegerField(choices=RatingChoices.choices, default=RatingChoices.zero.value)


class Attribute(BaseModel):
    name=models.CharField(max_length=255, null=True, blank=True)
    category=models.ForeignKey(Category, on_delete=models.CASCADE, related_name='attributes', null=True, blank=True)

    def __str__(self):
        return self.name
    
class AttributeValue(BaseModel):
    value=models.CharField(max_length=255, null=True, blank=True)
    attribute=models.ForeignKey(Attribute, on_delete=models.CASCADE,null=True, blank=True)
    product=models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_attributes', null=True, blank=True)


    def __str__(self):
        return self.value
    
# 




