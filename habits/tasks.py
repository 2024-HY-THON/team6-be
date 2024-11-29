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
    ).select_related('user')

    for category in categories:
        user = category.user
        habits = list(Habit.objects.filter(category=category))

        if habits:
            # 랜덤하게 Habit 선택 및 Category의 random_habit 업데이트
            habit = choice(habits)
            category.random_habit = habit
            category.save(update_fields=['random_habit'])

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

