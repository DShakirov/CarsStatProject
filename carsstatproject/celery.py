import os

from celery import Celery
from celery.schedules import crontab

from carsstatproject.settings import CELERY_BROKER_URL

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carsstatproject.settings')

#app = Celery('carsstatproject')
app = Celery('CarsStatProject')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'every': {
        'task': 'carsstat.tasks.parse',
        'schedule': crontab(minute=10, hour=19),  # change to `crontab(minute=0, hour=0)` if you want it to run daily at midnight
    },
}
