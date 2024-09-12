from django.db.models.signals import post_save, pre_save, pre_delete, post_delete

from books.models import Book, Author
from django.dispatch import receiver
from config.settings import EMAIL_DEFAULT_SENDER
from user.models import CustomUser
from django.core.mail import send_mail
# def pre_save_book(sender, instance, **kwargs):
#     print('Just a simple test!')

# pre_save.connect(pre_save_book, sender=Book)

# @receiver(post_save, sender=book)
# def post_save_book(sender, instance, **kwargs):
#     print('Okay, good')

@receiver(post_save, sender=Book)
def send_creation_notification(sender, instance, created, **kwargs):
    if created:
        subject = 'New book Notification'
        message = 'A new book has been added.'
        from_email = EMAIL_DEFAULT_SENDER
        recipient_list = [user.email for user in CustomUser.objects.all()]

        send_mail(subject, message, from_email, recipient_list)


@receiver(post_save, sender=Author)
def send_creation_notification(sender, instance, created, **kwargs):
    if created:
        subject = 'New author Notification'
        message = 'A new author has been added.'
        from_email = EMAIL_DEFAULT_SENDER
        recipient_list = [user.email for user in CustomUser.objects.all()]

        send_mail(subject, message, from_email, recipient_list)
