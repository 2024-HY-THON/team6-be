from django.db import models
from users.models import CustomUser  # users 앱의 CustomUser 모델 import

# Category 모델 정의
class Category(models.Model):
    category_id = models.BigAutoField(primary_key=True)  # 카테고리 ID
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # 유저 ID (Foreign Key)
    category = models.CharField(max_length=100)  # 카테고리 이름
    choose = models.BooleanField(default=False) # 카테고리 선택 여부
    #created = models.DateTimeField(auto_now_add=True)  # 작성 날짜
    #updated = models.DateTimeField(auto_now=True)  # 수정 날짜
    #button = models.BooleanField(default=False)  # 알람 선택 여부

    def __str__(self):
        return self.category


# Habit 모델 정의
class Habit(models.Model):
    habit_id = models.BigAutoField(primary_key=True)  # 습관 ID
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # 카테고리 ID (Foreign Key)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # 유저 ID (Foreign Key)
    content = models.JSONField()  # 습관 내용
    created = models.DateTimeField(auto_now_add=True)  # 작성 날짜
    updated = models.DateTimeField(auto_now=True)  # 수정 날짜

    def __str__(self):
        return self.content
