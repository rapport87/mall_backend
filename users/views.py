import os
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from . import serializers
import requests
from users.models import User
from rest_framework.exceptions import ParseError, NotFound


DEBUG = os.environ.get("DEBUG", "True") != "False"


class Profile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(
            user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            user = serializer.save()
            serializer = serializers.PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class Users(APIView):
    def post(self, request):
        password = request.data.get("password")
        if not password:
            raise ParseError
        serializer = serializers.PrivateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.save()
            serializer = serializers.PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class SignUp(APIView):
    def post(self, request):
        try:
            name = request.data.get("name")
            email = request.data.get("email")
            username = request.data.get("username")
            password = request.data.get("password")

            if User.objects.filter(name=name).exists():
                return Response(
                    {"fail": "해당 ID가 이미 존재합니다"},
                    status=status.HTTP_409_CONFLICT,
                )

            if User.objects.filter(email=email).exists():
                return Response(
                    {"fail": "이미 등록된 E-mail 주소 입니다"},
                    status=status.HTTP_409_CONFLICT,
                )

            user = User.objects.create(
                username=username,
                name=name,
                email=email,
            )
            user.set_password(password)
            user.save()
            login(request, user)
            return Response(
                {"success": "Signup is completed"}, status=status.HTTP_200_OK
            )
        except Exception:
            return Response(
                {"fail": f"{Exception}"}, status=status.HTTP_400_BAD_REQUEST
            )


class PublicUser(APIView):
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound
        serializer = serializers.PrivateUserSerializer(user)
        return Response(serializer.data)


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        if not old_password or not new_password:
            raise ParseError
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            raise ParseError


class LogIn(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            login(request, user)
            return Response({"ok": "Welcome!"})
        else:
            return Response(
                {"error": "wrong password"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class LogOut(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"ok": "bye!"})


class KakaoLogIn(APIView):
    def post(self, request):
        try:
            code = request.data.get("code")
            if DEBUG:
                redirect_uri = "http://127.0.0.1:3000/social/kakao"
            else:
                redirect_uri = "https://learninglab.co.kr:60000/social/kakao"

            access_token = requests.post(
                "https://kauth.kakao.com/oauth/token",
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data={
                    "grant_type": "authorization_code",
                    "client_id": "639900a71d5784dda0382e93d7ba14be",
                    "redirect_uri": redirect_uri,
                    "code": code,
                },
            )
            access_token = access_token.json().get("access_token")
            user_data = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
                },
            )
            user_data = user_data.json()
            kakao_id = f"{user_data.get('id')}@kakao"
            nickname = user_data.get("kakao_account").get("profile").get("nickname")

            try:
                user = User.objects.get(username=kakao_id)
            except User.DoesNotExist:
                user = User.objects.create(
                    username=kakao_id,
                    name=nickname,
                )
                user.set_unusable_password()
                user.save()

            login(request, user)
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
