from django.urls import path
from . import views
from .views import (
    UserRegistrationView, PasswordUpdateView, EmailUpdateView,
    NicknameUpdateView, UserDeleteView, UserDetailView,
    CheckDuplicateIDView, CheckDuplicateEmailView, CheckDuplicateNicknameView,
    AllUsersView, DeleteSpecificUserView, TestFCMNotification
)

urlpatterns = [
    path('user/register/', UserRegistrationView.as_view(), name='user_register'),  
    path('user/detail/', UserDetailView.as_view(), name='user_detail'),

    path('user/update/password/', PasswordUpdateView.as_view(), name='password_update'),  
    path('user/update/email/', EmailUpdateView.as_view(), name='email_update'),  
    path('user/update/nickname/', NicknameUpdateView.as_view(), name='nickname_update'),  

    path('user/delete/', UserDeleteView.as_view(), name='user_delete'),  

    path('user/duplicate/id/', CheckDuplicateIDView.as_view(), name='check-duplicate-id'),
    path('user/duplicate/email/', CheckDuplicateEmailView.as_view(), name='check-duplicate-email'),
    path('user/duplicate/nickname/', CheckDuplicateNicknameView.as_view(), name='check-duplicate-nickname'),

    path('user/admin/all/', AllUsersView.as_view(), name='all_users'),  
    path('user/admin/delete/<str:pk>/', DeleteSpecificUserView.as_view(), name='delete_specific_user'),  

    path('fcm/token/', views.update_fcm_token_view, name='update_fcm_token'),
    path('api/test-fcm-notification/', TestFCMNotification.as_view(), name='test_fcm_notification'),
]
