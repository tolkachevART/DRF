from rest_framework.serializers import ModelSerializer

from users.models import User, Payment


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "city", "avatar")


class UserProfileSerializer(ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True, source="user_payments")

    class Meta:
        model = User
        fields = ("id", "email", "phone", "city", "avatar", "payments", "date_joined", "last_name")
