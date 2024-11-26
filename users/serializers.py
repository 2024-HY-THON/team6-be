from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer) :
    password = serializers.CharField(write_only=True)

    class Meta :
        model = User
        fields = ['id', 'password', 'email', 'nickname']

    def create(self, validated_data) :
        user = User.objects.create_user(
            id=validated_data['id'],
            password=validated_data['password'],
            email=validated_data['email'],
            nickname=validated_data['nickname'],
        )
        return user