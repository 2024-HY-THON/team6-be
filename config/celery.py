from celery import Celery
from celery.schedules import schedule
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

app.conf.update(
    timezone='Asia/Seoul',  # 한국 시간대로 설정
    enable_utc=True,  # UTC 시간 사용 활성화
)

# Django 설정을 Celery에 로드
app.config_from_object('django.conf:settings', namespace='CELERY')

# Celery Beat 스케줄 설정
app.conf.beat_schedule = {
    'send_category_alarm_every_30_seconds': {
        'task': 'habits.tasks.send_category_alarm',  # 정확한 경로로 수정
        'schedule': schedule(30.0),  # 30초마다 실행
    },
}

app.autodiscover_tasks()

broker_url = 'amqp://mine:mine@3.223.239.126//'
