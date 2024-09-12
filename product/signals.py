from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
import json 
import os 
from pathlib import Path
from django.conf import settings
from django.http import JsonResponse
from django.forms.models import model_to_dict

from product.models import Product, Category, Image, Comment, Attribute, AttributeValue
from django.dispatch import receiver
from config.settings import EMAIL_DEFAULT_SENDER
from user.models import CustomUser
from django.core.mail import send_mail
def pre_save_product(sender, instance, **kwargs):
    print('No idea what I am doing')

pre_save.connect(pre_save_product, sender=Product)

# @receiver(post_save, sender=Product)
# def post_save_product(sender, instance, **kwargs):
#     print('Okay, good')

@receiver(post_save, sender=Product)
def send_creation_notification(sender, instance, created, **kwargs):
    if created:
        subject = 'New Product Notification'
        message = 'A new product has been added.'
        from_email = EMAIL_DEFAULT_SENDER
        recipient_list = [user.email for user in CustomUser.objects.all()]

        send_mail(subject, message, from_email, recipient_list)


@receiver(post_save, sender=Category)
def send_creation_notification(sender, instance, created, **kwargs):
    if created:
        subject = 'New category Notification'
        message = 'A new category has been added.'
        from_email = EMAIL_DEFAULT_SENDER
        recipient_list = [user.email for user in CustomUser.objects.all()]

        send_mail(subject, message, from_email, recipient_list)


@receiver(post_save, sender=Image)
def send_creation_notification(sender, instance, created, **kwargs):
    if created:
        subject = 'New image Notification'
        message = 'A new image has been added.'
        from_email = EMAIL_DEFAULT_SENDER
        recipient_list = [user.email for user in CustomUser.objects.all()]

        send_mail(subject, message, from_email, recipient_list)


@receiver(post_save, sender=Comment)
def send_creation_notification(sender, instance, created, **kwargs):
    if created:
        subject = 'New comment Notification'
        message = 'A new comment has been added.'
        from_email = EMAIL_DEFAULT_SENDER
        recipient_list = [user.email for user in CustomUser.objects.all()]

        send_mail(subject, message, from_email, recipient_list)


@receiver(post_save, sender=Attribute)
def send_creation_notification(sender, instance, created, **kwargs):
    if created:
        subject = 'New attribute Notification'
        message = 'A new attribute has been added.'
        from_email = EMAIL_DEFAULT_SENDER
        recipient_list = [user.email for user in CustomUser.objects.all()]

        send_mail(subject, message, from_email, recipient_list)


@receiver(post_save, sender=AttributeValue)
def send_creation_notification(sender, instance, created, **kwargs):
    if created:
        subject = 'New attribute_value Notification'
        message = 'A new attribute_value has been added.'
        from_email = EMAIL_DEFAULT_SENDER
        recipient_list = [user.email for user in CustomUser.objects.all()]

        send_mail(subject, message, from_email, recipient_list)


# @receiver(pre_delete, sender=Product)
# def send_deletion_notification(sender, instance, **kwargs):
#     fixture_path = Path(os.path.join(settings.BASE_DIR, "product", "product_data", "products_deleted.json"))
#     category_instance=JsonResponse(model_to_dict(instance.category))
#     data={
#         'id':instance.id,
#         'name':instance.name,
#         'description':instance.description,
#         'price': instance.price,
#         'category':category_instance,
#         'discount':instance.discount,
#         'quantity':instance.quantity,
#         'slug': instance.slug
#     }

#     with open(fixture_path, 'a+') as f:

#         if fixture_path.suffix == ".json":
#             fixture = json.dump(data, f, indent=4)
#             subject = 'Another product Notification'
#             message = 'Another product has been deleted.'
#             from_email = EMAIL_DEFAULT_SENDER
#             recipient_list = [user.email for user in CustomUser.objects.all()]

#             send_mail(subject, message, from_email, recipient_list)
#         else:
#             fixture = f.read()
#         return fixture
        

@receiver(pre_delete, sender=Product)
def send_deletion_notification(sender, instance, **kwargs):
    fixture_path = Path(os.path.join(settings.BASE_DIR, "product", "product_data", "products_deleted.json"))
    
    # Convert category to a dictionary
    category_instance = model_to_dict(instance.category) if instance.category else {}
    
    data = {
        'id': instance.id,
        'name': instance.name,
        'description': instance.description,
        'price': instance.price,
        'category': category_instance,
        'discount': instance.discount,
        'quantity': instance.quantity,
        'slug': instance.slug
    }

    with open(fixture_path, 'a+') as f:
        if fixture_path.suffix == ".json":
            # Write the data as a JSON object
            json.dump(data, f, indent=4)
            f.write(",\n")  # Add a comma for the next entry if needed

            subject = 'Another product Notification'
            message = 'Another product has been deleted.'
            from_email = EMAIL_DEFAULT_SENDER
            recipient_list = [user.email for user in CustomUser.objects.all()]

            send_mail(subject, message, from_email, recipient_list)
        else:
            f.seek(0)  # Move to the beginning of the file
            fixture = f.read()
    
    return None  # No need to return anything here