from django.urls import path

from users.apps import UsersConfig
from users.views import UserProfileUpdateAPIView, PaymentListAPIView

app_name = UsersConfig.name

urlpatterns = [
    path("user/<int:pk>/update/", UserProfileUpdateAPIView.as_view(), name="user_update"),
    path("payment/", PaymentListAPIView.as_view(), name="payment_list"),
]
