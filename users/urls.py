from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.apps import UsersConfig
from users.views import UserProfileUpdateAPIView, PaymentListAPIView, UserCreateAPIView, UserListAPIView, \
    UserProfileRetrieveAPIView, UserProfileDestroyAPIView

app_name = UsersConfig.name

urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path("user/", UserListAPIView.as_view(), name="user-list"),
    path("user/<int:pk>/", UserProfileRetrieveAPIView.as_view(), name="user-retrieve"),
    path("user/<int:pk>/update", UserProfileUpdateAPIView.as_view(), name="user-update"),
    path("user/<int:pk>/delete", UserProfileDestroyAPIView.as_view(), name="user-destroy"),
    path("payment/", PaymentListAPIView.as_view(), name="payment-list"),
    path("login/",TokenObtainPairView.as_view(permission_classes=(AllowAny,)),name="login",),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]
