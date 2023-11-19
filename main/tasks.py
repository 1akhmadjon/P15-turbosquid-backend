from celery import shared_task
from django.core.mail import send_mail
from django.urls import reverse, reverse_lazy


@shared_task
def send_email(emails: list, products):
    send_mail(
        subject='Uploaded new product',
        message=f"""
Name: {products['name']}
Description: {products['description']}
Price: {products['price']}
Link: http://127.0.0.1:8080/api/product/{products['slug']}
    """,
        from_email='From 1Team',
        recipient_list=emails,
        fail_silently=True
    )
    return 'Done'
