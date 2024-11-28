from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Category
from .serializers import CategorySerializer, HabitCreateSerializer
from django.shortcuts import get_object_or_404
from users.models import CustomUser  # CustomUser 모델 import

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