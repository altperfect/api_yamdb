from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import CommentViewSet, ReviewViewSet, UserViewSet

v1_router = DefaultRouter()
v1_router.register(
    r'titles/(?P<title_id>/d+)/reviews/(?P<review_id>/d+)/comments',
    CommentViewSet,
    basename='comment'
)
v1_router.register(
    r'titles/(?P<title_id>/d+)/reviews/',
    ReviewViewSet,
    basename='review'
)
v1_router.register(
    'users',
    UserViewSet,
    basename='users'
)

urlpatterns = [
    path('v1/auth/', include('users.urls')),
    path("v1/", include(v1_router.urls)),
]
