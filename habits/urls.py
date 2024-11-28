from django.urls import path
from .views import UserCategoryList, CategoryDelete, HabitCreate

urlpatterns = [
    path('<str:user_id>/', UserCategoryList.as_view(), name='user-category-list'),
    path('delete/<int:category_id>/', CategoryDelete.as_view(), name='category-delete'),
    path('create/<str:user_id>/', HabitCreate.as_view(), name='habit-create'),
]
