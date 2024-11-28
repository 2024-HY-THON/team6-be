from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('id', 'email', 'nickname', 'is_staff', 'is_active')  # 표시할 필드
    fieldsets = (  # 수정 페이지에서 보이는 필드 그룹
        (None, {'fields': ('id', 'email', 'nickname', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (  # 사용자 추가 페이지에서 보이는 필드 그룹
        (None, {
            'classes': ('wide',),
            'fields': ('id', 'email', 'nickname', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )
    search_fields = ('id', 'email', 'nickname')  # 검색 가능 필드
    ordering = ('id',)  # 정렬 기준
