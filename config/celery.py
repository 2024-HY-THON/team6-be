# config/celery.py
from celery import Celery
from datetime import timedelta
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'send_category_alarm_every_minute': {
        'task': 'send_category_alarm',
        'schedule': timedelta(minutes=1),  # 1분마다 작업을 실행
    },
}

app.autodiscover_tasks()

broker_url = 'amqp://mine:mine@3.223.239.126//'