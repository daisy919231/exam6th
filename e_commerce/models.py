from django.db import models
from django.utils.text import slugify
from django.template.defaultfilters import date

class BaseModel(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True

class Customer(BaseModel):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=80)
    email=models.EmailField(unique=True)
    phone_num=models.CharField(max_length=15)
    bill_address=models.CharField(max_length=100)
    image=models.ImageField(upload_to='customers', default='default_user.jpg')
    slug=models.SlugField(null=True, blank=True)


    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug=slugify(self.full_name)
        super(Customer,self).save(*args, **kwargs)

    class Meta:
        db_table='Customers'

    
    
    @property
    def full_name(self):
        return f'{self.first_name}  {self.last_name}'
    
    def __str__(self):
        return self.full_name
    
    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug=slugify(self.full_name)
        super(Customer,self).save(*args, **kwargs)

    
    @property
    def joined_at(self):
        if self.created_at is not None:
            joined=self.created_at.strftime('%Y-%m-%d')
            return joined
    @property
    def rounded_circle(self):
        fl=self.first_name[0]
        sl=self.last_name[0]
        return f'{fl} {sl}'


# Create your models here.
