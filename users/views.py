from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

User = get_user_model()

# 1. 회원가입 기능
class UserRegistrationView(APIView):
    def post(self, request):
        data = request.data
        if User.objects.filter(id=data.get('id')).exists():
            return Response({"error": "중복된 ID입니다."}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=data.get('email')).exists():
            return Response({"error": "중복된 이메일입니다."}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(nickname=data.get('nickname')).exists():
            return Response({"error": "중복된 닉네임입니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(
            id=data['id'],
            password=data['password'],
            email=data['email'],
            nickname=data['nickname']
        )
        return Response({"message": "회원가입이 성공적으로 완료되었습니다."}, status=status.HTTP_201_CREATED)

# 2. 로그인 한 user의 정보 조회
class UserDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "email": user.email,
            "nickname": user.nickname,
        }, status=status.HTTP_200_OK)

# 3. 로그인 한 user의 비밀번호 수정 기능
class PasswordUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        user = request.user
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')

        if not check_password(current_password, user.password):
            return Response({"error": "현재 비밀번호가 올바르지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()
        return Response({"message": "비밀번호가 성공적으로 변경되었습니다."}, status=status.HTTP_200_OK)

# 4. 로그인 한 user의 이메일 수정 기능
class EmailUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        user = request.user
        new_email = request.data.get('new_email')

        if User.objects.filter(email=new_email).exists():
            return Response({"error": "이미 사용 중인 이메일입니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        user.email = new_email
        user.save()
        return Response({"message": "이메일이 성공적으로 변경되었습니다."}, status=status.HTTP_200_OK)

# 5. 로그인 한 user의 닉네임 수정 기능
class NicknameUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        user = request.user
        new_nickname = request.data.get('new_nickname')

        if User.objects.filter(nickname=new_nickname).exists():
            return Response({"error": "이미 사용 중인 닉네임입니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        user.nickname = new_nickname
        user.save()
        return Response({"message": "닉네임이 성공적으로 변경되었습니다."}, status=status.HTTP_200_OK)

# 6. 로그인 한 user의 탈퇴 기능
class UserDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({"message": "계정이 성공적으로 삭제되었습니다."}, status=status.HTTP_200_OK)

# 7. ID 중복 확인
class CheckDuplicateIDView(APIView):
    def post(self, request):
        user_id = request.data.get("id", None)
        if not user_id:
            return Response({"message": "ID를 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(id=user_id).exists():
            return Response({"message": "중복된 ID입니다."}, status=status.HTTP_409_CONFLICT)
        return Response({"message": "사용 가능한 ID입니다."}, status=status.HTTP_200_OK)

# 8. 이메일 중복 확인
class CheckDuplicateEmailView(APIView):
    def post(self, request):
        email = request.data.get("email", None)
        if not email:
            return Response({"message": "이메일을 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({"message": "중복된 이메일입니다."}, status=status.HTTP_409_CONFLICT)
        return Response({"message": "사용 가능한 이메일입니다."}, status=status.HTTP_200_OK)

# 9. 닉네임 중복 확인
class CheckDuplicateNicknameView(APIView):
    def post(self, request):
        nickname = request.data.get("nickname", None)
        if not nickname:
            return Response({"message": "닉네임을 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(nickname=nickname).exists():
            return Response({"message": "중복된 닉네임입니다."}, status=status.HTTP_409_CONFLICT)
        return Response({"message": "사용 가능한 닉네임입니다."}, status=status.HTTP_200_OK)

# 10. 모든 user 정보 조회 (관리자만 가능)
class AllUsersView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        users = User.objects.all()
        user_data = [{"id": user.id, "email": user.email, "nickname": user.nickname} for user in users]
        return Response(user_data, status=status.HTTP_200_OK)

# 11. 특정 user 삭제 (관리자만 가능)
class DeleteSpecificUserView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            user.delete()
            return Response({"message": "사용자가 성공적으로 삭제되었습니다."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "사용자를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
