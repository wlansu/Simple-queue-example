import os

from django.conf import settings

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sendcloud.settings")

app = Celery("sendcloud_assignment")

app.config_from_object(settings, namespace="CELERY")

app.autodiscover_tasks()
