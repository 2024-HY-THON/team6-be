from django.urls import path
from .views import UserCategoryList, CategoryDelete, CategoryCreate, CategoryContent, UpdateContent, ActionCreate, MainPage, CategoryAlarmTimeUpdate, CategoryRandomHabitView, TriggerAlarmTask, UserAction


urlpatterns = [
    path('<str:user_id>/', UserCategoryList.as_view(), name='user-category-list'),
    path('delete/<int:category_id>/', CategoryDelete.as_view(), name='category-delete'),
    path('create/<str:user_id>/', CategoryCreate.as_view(), name='category_create'),
    path('content/<str:user_id>/<int:category_id>/', CategoryContent.as_view(), name='user_category_content'),
    path('update/<str:user_id>/<int:category_id>/', UpdateContent.as_view(), name='update_category_or_content'),
    path('action/create/', ActionCreate.as_view(), name='action_create'),
    path('main/<str:user_id>/', MainPage.as_view(), name='user_selected_categories'),
    path('action/<str:user_id>/', UserAction.as_view(), name='user_action_summary'),


    path('alarm/update/<str:user_id>/<int:category_id>/', CategoryAlarmTimeUpdate.as_view(), name='category-alarm-time-update'),

    path('random/habit/<str:user_id>/', CategoryRandomHabitView.as_view(), name='category-random-habit'),

    path('trigger-alarm/<int:category_id>/', TriggerAlarmTask.as_view(), name='trigger_alarm_task'),
]
