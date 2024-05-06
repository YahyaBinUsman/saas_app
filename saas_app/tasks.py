# tasks.py

from celery import shared_task
from django.core.mail import send_mail

@shared_task
def process_task(email, message):
    # Send an email asynchronously
    send_mail(
        'Subject here',
        message,
        'from@example.com',
        [email],
        fail_silently=False,
    )
