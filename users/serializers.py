from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Subscription
from materials.serializers import SubscriptionSerializer
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
    subscriptions = SerializerMethodField()

    def get_subscriptions(self, obj):
        subscriptions = Subscription.objects.filter(user=obj)
        return SubscriptionSerializer(subscriptions, many=True).data

    class Meta:
        model = User
        fields = ("id", "email", "phone", "city", "avatar", "payments", "date_joined", "last_name""subscriptions",)
