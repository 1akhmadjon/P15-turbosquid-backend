import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'P15turbosquid.settings')

app = Celery('P15turbosquid')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
