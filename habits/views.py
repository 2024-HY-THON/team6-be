from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Habit, Action
from .serializers import CategorySerializer, HabitCreateSerializer, RandomHabitSerializer
from django.shortcuts import get_object_or_404
from users.models import CustomUser  # CustomUser 모델 import
from django.utils.timezone import now
from rest_framework.permissions import IsAuthenticated
import random
from django.db.models import Prefetch

from .tasks import send_category_alarm


class UserCategoryList(APIView):
    def get(self, request, user_id):
        # user_id에 해당하는 사용자 가져오기
        user = get_object_or_404(CustomUser, id=user_id)

        # 해당 사용자의 Category 데이터 가져오기
        categories = Category.objects.filter(user=user)
        
        # 직렬화하여 반환
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CategoryDelete(APIView):
    def delete(self, request, category_id):
        # category_id에 해당하는 카테고리 가져오기
        category = get_object_or_404(Category, category_id=category_id)
        
        # 카테고리 삭제
        category.delete()
        
        # 성공 응답 반환
        return Response(
            {"message": "Category deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )

class CategoryCreate(APIView):
    def post(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)

        category_name = request.data.get("category")
        if not category_name:
            return Response(
                {"error": "Category name is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        category = Category.objects.create(user=user, category=category_name)

        serializer = CategorySerializer(category)
        return Response(
            {
                "message": "Category created successfully.",
                "category": serializer.data
            },
            status=status.HTTP_201_CREATED
        )


class HabitCreate(APIView):
    def post(self, request, user_id):
        # 사용자 가져오기
        user = get_object_or_404(CustomUser, id=user_id)

        # 요청 데이터 직렬화
        serializer = HabitCreateSerializer(data=request.data, context={'user': user})
        if serializer.is_valid():
            serializer.save()  # 데이터 저장
            return Response({"message": "Habits saved successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CategoryContent(APIView):
    def get(self, request, user_id, category_id):
        # user_id에 해당하는 사용자 확인
        user = get_object_or_404(CustomUser, id=user_id)
        
        # category_id에 해당하는 카테고리 확인
        category = get_object_or_404(Category, category_id=category_id, user=user)

        # 해당 카테고리와 사용자와 관련된 Habit 불러오기
        habits = Habit.objects.filter(user=user, category=category).values_list('content', flat=True)

        # habits가 존재하지 않을 경우 처리
        if not habits:
            return Response({"message": "No content found for the given user and category"}, status=status.HTTP_404_NOT_FOUND)

        # content 반환
        return Response({"contents": list(habits)}, status=status.HTTP_200_OK)

class UpdateContent(APIView):
    def put(self, request, user_id, category_id):
        # user_id에 해당하는 사용자 확인
        user = get_object_or_404(CustomUser, id=user_id)

        # category_id에 해당하는 카테고리 확인
        category = get_object_or_404(Category, category_id=category_id, user=user)

        # 요청 데이터에서 수정할 항목 확인
        category_name = request.data.get("category")  # 수정할 카테고리 이름
        habits = request.data.get("habits")  # 수정할 습관 리스트

        # 카테고리 수정
        if category_name:
            category.category = category_name
            category.save()

        # Habit 수정
        if habits:
            # 기존 Habits 삭제
            Habit.objects.filter(category=category, user=user).delete()

            # 새로운 Habit 추가
            for habit_content in habits:
                Habit.objects.create(
                    category=category,
                    user=user,
                    content=habit_content
                )

        return Response(
            {"message": "Category and/or Habits updated successfully"},
            status=status.HTTP_200_OK
        )
    
class ActionCreate(APIView):
    def post(self, request):
        habit_id = request.data.get("habit_id")
        do_or_not = request.data.get("do_or_not")

        if habit_id is None or do_or_not is None:
            return Response(
                {"error": "Both 'habit_id' and 'do_or_not' fields are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        habit = get_object_or_404(Habit, habit_id=habit_id)

        Action.objects.create(
            habit=habit,
            do_or_not=do_or_not
        )

        today = now().date()

        today_actions = Action.objects.filter(
            habit__user=habit.user,
            created=today
        )

        completed_count = today_actions.filter(do_or_not=True).count()
        not_completed_count = today_actions.filter(do_or_not=False).count()

        return Response(
            {
                "message": "Action created successfully.",
                "completed_count": completed_count,
                "not_completed_count": not_completed_count
            },
            status=status.HTTP_201_CREATED
        )

class UserAction(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)

        today = now().date()

        today_actions = Action.objects.filter(
            habit__user=user,
            created=today
        )

        completed_count = today_actions.filter(do_or_not=True).count()
        not_completed_count = today_actions.filter(do_or_not=False).count()

        response_data = {
            "completed_count": completed_count,
            "not_completed_count": not_completed_count
        }

        return Response(response_data, status=200)



class MainPage(APIView):
    def get(self, request, user_id):
        # user_id에 해당하는 사용자 확인
        user = get_object_or_404(CustomUser, id=user_id)

        # 현재 날짜 가져오기
        today = now().date()

        # choose가 True인 Category와 관련된 Habit 데이터 가져오기
        categories = Category.objects.filter(user=user, choose=True)

        # 결과 데이터 생성
        result = []

        # 카테고리와 습관 데이터 구성
        for category in categories:
            # 해당 카테고리와 연결된 Habit 데이터 가져오기
            habits = Habit.objects.filter(category=category)

            # 카테고리와 해당 습관 데이터 추가
            category_data = {
                "category": category.category,
                "contents": [habit.content for habit in habits]
            }
            result.append(category_data)

        # Action 테이블에서 오늘 날짜와 관련된 실천 데이터 가져오기
        # Habit과 연결된 Action을 통해 필터링
        today_actions = Action.objects.filter(
            habit__user=user,  # Habit 모델을 통해 사용자 필터링
            created=today
        )

        # 실천 여부를 기반으로 개수 계산
        completed_count = today_actions.filter(do_or_not=True).count()
        not_completed_count = today_actions.filter(do_or_not=False).count()

        # 실천 결과 개수를 result에 추가
        result.append({
            "completed_count": completed_count,
            "not_completed_count": not_completed_count
        })

        # 결과 반환
        return Response(result, status=200)
    
# 알림 시간 설정
class CategoryAlarmTimeUpdate(APIView):
    def put(self, request, user_id, category_id):
        user = get_object_or_404(CustomUser, id=user_id)
        category = get_object_or_404(Category, category_id=category_id, user=user)
        
        alarm_time = request.data.get("alarm_time")
        if alarm_time:
            category.alarm_time = alarm_time
            category.save()
            return Response({"message": "알람 시간이 업데이트 되었습니다."}, status=status.HTTP_200_OK)
        
        return Response({"error": "유효하지 않은 알람시간입니다."}, status=status.HTTP_400_BAD_REQUEST)

# 선택 여부
class UpdateCategoryChooseView(APIView):
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

    def patch(self, request, category_id):
        try:
            # 해당 카테고리를 가져옵니다.
            category = Category.objects.get(category_id=category_id, user=request.user)
        except Category.DoesNotExist:
            return Response({"error": "Category not found."}, status=status.HTTP_404_NOT_FOUND)

        # 요청 데이터에서 'choose' 값을 가져옵니다.
        choose_value = request.data.get('choose')
        if choose_value is None:
            return Response({"error": "'choose' field is required."}, status=status.HTTP_400_BAD_REQUEST)

        # 'choose' 값을 업데이트합니다.
        category.choose = choose_value
        category.save()

        # 직렬화 후 반환합니다.
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CategoryRandomHabitView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            user = get_object_or_404(CustomUser, id=user_id)

            categories = Category.objects.filter(
                user=user, choose=True
            ).prefetch_related(
                Prefetch('habit_set', queryset=Habit.objects.filter(user=user))
            )

            if not categories:
                return Response({'error': 'No categories with choose=True found.'}, status=404)

            category = random.choice(categories)

            habits = category.habit_set.all()

            if not habits:
                return Response({'error': f'No habits found for category {category.category}.'}, status=404)

            random_habit = random.choice(habits)

            return Response({
                'category': category.category,
                'random_habit': {
                    'habit_id': random_habit.habit_id,
                    'content': random_habit.content
                }
            }, status=200)

        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found.'}, status=404)


class TriggerAlarmTask(APIView):
    def post(self, request, category_id):
        # Celery 작업을 트리거하는 코드
        send_category_alarm.apply_async(kwargs={'category_id': category_id})
        return Response({"message": "알림 작업이 큐에 추가되었습니다."}, status=status.HTTP_200_OK)