from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_email(emails: list, product):
    send_mail(
        subject='Uploaded new Product',
        message=f'''
Title: {product['title']}
Description: {product['description']}
Price: {product['price']}
Link: http://127.0.0.1:8000/product-update/{product['id']}
        ''',
        from_email='From P15Team',
        recipient_list=emails,
        fail_silently=True
    )
    return 'Done'
