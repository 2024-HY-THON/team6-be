from rest_framework import serializers
from .models import Category, Habit
from datetime import datetime

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'  # 모든 필드를 직렬화

class HabitCreateSerializer(serializers.Serializer):
    category_name = serializers.CharField(max_length=100)  # 카테고리 이름
    habits = serializers.ListField(  # 습관 리스트
        child=serializers.CharField(),  # 각 습관은 단순 문자열
        write_only=True
    )

    def create(self, validated_data):
        user = self.context['user']  # View에서 전달된 사용자
        category_name = validated_data['category_name']
        habits_data = validated_data['habits']

        # 카테고리 가져오거나 생성
        category, created = Category.objects.get_or_create(
            user=user,
            category=category_name
        )

        # 습관 데이터 저장
        for habit_content in habits_data:
            Habit.objects.create(
                category=category,
                user=user,
                content=habit_content,
                created=datetime.now(),
                updated=datetime.now()
            )

        return category