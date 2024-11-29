from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, id, email, nickname, password=None, **extra_fields):
        if not id:
            raise ValueError("사용자 ID는 반드시 입력해야 합니다.")
        if not email:
            raise ValueError("이메일은 반드시 입력해야 합니다.")
        if not nickname:
            raise ValueError("닉네임은 반드시 입력해야 합니다.")
        
        email = self.normalize_email(email)
        user = self.model(id=id, email=email, nickname=nickname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, id, email, nickname, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("관리자는 반드시 is_staff=True 여야 합니다.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("관리자는 반드시 is_superuser=True 여야 합니다.")

        return self.create_user(id, email, nickname, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.CharField(max_length=50, unique=True, primary_key=True) 
    email = models.EmailField(unique=True)  
    nickname = models.CharField(max_length=30, unique=True)  
    password = models.CharField(max_length=128)  
    is_active = models.BooleanField(default=True)  
    is_staff = models.BooleanField(default=False)  
    fcm_token = models.CharField(max_length=255, blank=True, null=True)  # FCM 토큰 필드 추가

    objects = CustomUserManager()

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['email', 'nickname']  

    def __str__(self):
        return self.id
