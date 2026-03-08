from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import *
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings


@receiver(post_save, sender=User)
def send_email(sender, instance, created, args, *kwargs):
    if created:
        # user = instance
        email = instance.email
        username = instance.username
        html_email = render_to_string( 'welcome_email.html' ,{
            'user' : username,
        })
        
        welcome_email = EmailMessage(
            f'Welcome To Chatflow, {username}',
            html_email,
            settings.EMAIL_HOST_USER,
            [email],
        )
        
        welcome_email.content_subtype = 'html'
        welcome_email.fail_silently = True
        welcome_email.send()
        
        