from django.urls import path

from users.views import APIObtainToken, APISignUp

urlpatterns = [
    path("signup/", APISignUp.as_view(), name="token_signup"),
    path(
        "token/",
        APIObtainToken.as_view(),
        name="token_obtain",
    ),
]
