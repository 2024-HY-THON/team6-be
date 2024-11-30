from celery import shared_task
from datetime import datetime
from .models import Category, Habit
from config.fcm import send_alarm_message
from random import choice
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True, acks_late=True)
def send_category_alarm(self, category_id=None):
    now = datetime.now()

    # 카테고리 필터링
    categories = Category.objects.filter(
        category_id=category_id,
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

            # token = user.fcm_token  # 유저의 FCM 토큰 가져오기
            token = "dh7WSNisRFWeHLLue9bc-S:APA91bGvhNtXeY3sIeyLGCLGAr3FOyqIpGKr3333_aRr5mf7__4nOLGBSs9CWAFP8aSn5R91n2sdvjitTOawqPtmK8dvQ7OCNb8qMcMiYTH8knDX36qf_BY"

            message_title = f"알림: {category.category}"
            message_body = f"오늘의 습관: {habit.content}"

            # 메시지 로그 출력
            logger.info(f"메시지 제목: {message_title}")
            logger.info(f"메시지 내용: {message_body}")

            if token:
                try:
                    send_alarm_message(
                        token,
                        f"알림: {category.category}",
                        f"오늘의 습관: {habit.content}"
                    )
                except Exception as e:
                    print(f"FCM 메시지 전송 실패: {e}")
            else:
                print(f"유효하지 않은 FCM 토큰: {token} - 카테고리: {category.category}")
