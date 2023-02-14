from django.conf import settings
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from users.models import User
from users.serializers import SignUpSerializer, TokenSerializer


class APISignUp(APIView):
    """
    Регистрация пользователя.
    Анонимный пользователь отправляет 'username' и 'email' в формате JSON
    и получает на почту код подтверждения.
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get("username")
        email = serializer.validated_data.get("email")

        try:
            user, created = User.objects.get_or_create(
                username=username,
                email=email
            )
        except IntegrityError:
            return Response(
                serializer.data, status=status.HTTP_400_BAD_REQUEST
            )
        else:
            if created:
                user.save()

        self.send_confirmation(user, request.data.get("email"))
        return Response(
            serializer.validated_data,
            status=status.HTTP_200_OK
        )

    def send_confirmation(self, user, email):
        send_mail(
            u"Код подтверждения для создания токена.",
            f"Ваш код: {user.confirmation_code}",
            settings.DEBUG_MAIL,
            [email],
            fail_silently=False,
        )


class APIObtainToken(APIView):
    """Создание JWT-токена."""
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get("username")
        confirmation_code = serializer.validated_data.get("confirmation_code")

        if not User.objects.filter(username=username).exists():
            return Response(status=status.HTTP_404_NOT_FOUND)

        if not User.objects.filter(
            confirmation_code=confirmation_code
        ).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(
            User,
            username=username,
            confirmation_code=confirmation_code
        )
        token = AccessToken.for_user(user)
        response = {
            "token": str(token)
        }
        return Response(
            response, status=status.HTTP_200_OK
        )
