from celery import shared_task
from datetime import datetime
from .models import Category, Habit
from config.fcm import send_alarm_message
from random import choice

@shared_task(bind=True, acks_late=True)
def send_category_alarm(self):
    now = datetime.now()

    # 알람 시간이 현재 시간과 일치하는 카테고리 조회
    categories = Category.objects.filter(
        choose=True,
        alarm_time__hour=now.hour,
        alarm_time__minute=now.minute
    ).select_related('user')  # 유저 정보 최적화

    for category in categories:
        user = category.user  # 연관된 유저
        habits = list(Habit.objects.filter(category=category))

        if habits:
            habit = choice(habits)  # 랜덤으로 습관 선택
            token = user.fcm_token  # 유저의 FCM 토큰 가져오기
            
            if token:
                try:
                    send_alarm_message(
                        token,
                        f"알림: {category.category}",
                        f"오늘의 습관: {habit.content}"
                    )
                except Exception as e:
                    # 예외 발생 시 로깅
                    print(f"FCM 메시지 전송 실패: {e}")
