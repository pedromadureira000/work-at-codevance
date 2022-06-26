import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')

app = Celery('settings')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.conf.enable_utc = False
app.conf.update(timezone='America/Sao_Paulo')
app.config_from_object(settings, namespace='CELERY')

# Celery Beat Settings
app.conf.beat_schedule = {
    #  'sometest': {
            #  'task': 'payment.tasks.test_func',
            #  'schedule': crontab(hour=0, minute=46, day_of_month=19, month_of_year = 6),
            #'args': (2,)
        #  }
}

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
