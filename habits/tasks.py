from celery import shared_task
from datetime import datetime
from .models import Category, Habit
from config.fcm import send_alarm_message
from random import choice
import logging
from django.utils import timezone

logger = logging.getLogger(__name__)

@shared_task(bind=True, acks_late=True)
def send_category_alarm(self, category_id=None):
    try:
        now = timezone.localtime(timezone.now())

        # 카테고리 필터링
        categories = Category.objects.filter(
            category_id=category_id,
            choose=True,
            alarm_time__hour=now.hour,
            alarm_time__minute=now.minute
        ).select_related('user')

        if not categories.exists():
            logger.warning(f"카테고리를 찾을 수 없습니다. category_id={category_id}")
            return

        for category in categories:
            user = category.user
            try:
                habits = list(Habit.objects.filter(category=category))

                if not habits:
                    logger.warning(f"카테고리에 연결된 습관이 없습니다. 카테고리: {category.category}")
                    continue

                # 랜덤하게 Habit 선택 및 Category의 random_habit 업데이트
                habit = choice(habits)
                category.random_habit = habit
                category.save(update_fields=['random_habit'])
                logger.info(f"랜덤 습관이 업데이트되었습니다. 카테고리: {category.category} -> {habit.content}")

                # 유저의 FCM 토큰 가져오기
                token = user.fcm_token or "dh7WSNisRFWeHLLue9bc-S:APA91bGvhNtXeY3sIeyLGCLGAr3FOyqIpGKr3333_aRr5mf7__4nOLGBSs9CWAFP8aSn5R91n2sdvjitTOawqPtmK8dvQ7OCNb8qMcMiYTH8knDX36qf_BY"

                if not token:
                    logger.warning(f"유효하지 않은 FCM 토큰입니다. 사용자 ID: {user.id}, 카테고리: {category.category}")
                    continue

                # 메시지 생성
                message_title = f"알림: {category.category}"
                message_body = f"오늘의 습관: {habit.content}"

                logger.info(f"메시지 전송 중 -> 제목: {message_title}, 내용: {message_body}")

                # FCM 메시지 전송
                send_alarm_message(token, message_title, message_body)

            except Exception as e:
                logger.error(f"카테고리 '{category.category}' 처리 중 오류 발생: {e}", exc_info=True)

    except Exception as e:
        logger.critical(f"send_category_alarm 작업에서 치명적인 오류 발생: {e}", exc_info=True)
