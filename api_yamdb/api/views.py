from django.conf import settings
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from api.permissions import IsAdmin, IsAdminModeratorAuthor
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    SignUpSerializer,
    TitleSerializer,
    TokenSerializer,
    UserSerializer,
)
from reviews.models import Category, Genre, Review, Title, User


class GenreViewSet(viewsets.ModelViewSet):
    """Вьюсет жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdmin,)


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет произведений."""
    queryset = Title.objects.annotate(
        review_rating=Avg('reviews__score'),
        rating=Avg("reviews__score")
    ).select_related(
        "category"
    ).prefetch_related(
        "genre"
    ).all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdmin,)


class CategoryViewSet(viewsets.ModelViewSet):
    """Вьюсет категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdmin,)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Создание и обработка комментариев.
    Права доступа: Админ, Модератор, Автор.
    """
    serializer_class = CommentSerializer
    permission_classes = (IsAdminModeratorAuthor,)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Создание и обработка отзывов.
    Права доступа: Админ, Модератор, Автор.
    """
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorAuthor,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет пользователя."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = "username"
    search_fields = ("username",)
    filter_backends = (SearchFilter,)
    http_method_names = ["get", "post", "delete", "patch"]

    @action(
        detail=False,
        methods=['GET', 'PATCH'],
        permission_classes=(permissions.IsAuthenticated,),
        url_path='me'
    )
    def me(self, request):
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
