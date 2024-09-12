from django.db.models.signals import post_save, pre_save, pre_delete, post_delete

from e_commerce.models import Customer
from django.dispatch import receiver
from config.settings import EMAIL_DEFAULT_SENDER
from user.models import CustomUser
from django.core.mail import send_mail
def pre_save_customer(sender, instance, **kwargs):
    print(' A simple pre_save signal test')

pre_save.connect(pre_save_customer, sender=Customer)

# @receiver(post_save, sender=customer)
# def post_save_customer(sender, instance, **kwargs):
#     print('Okay, good')

@receiver(post_save, sender=Customer)
def send_creation_notification(sender, instance, created, **kwargs):
    if created:
        subject = 'New customer Notification'
        message = 'A new customer has been added.'
        from_email = EMAIL_DEFAULT_SENDER
        recipient_list = [user.email for user in CustomUser.objects.all()]

        send_mail(subject, message, from_email, recipient_list)