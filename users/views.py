from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from users.models import User, Payment
from users.permissions import IsOwner
from users.serializers import UserSerializer, PaymentSerializer, UserProfileSerializer
from users.services import create_stripe_price, create_stripe_session


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        user_data = []
        for user in queryset:
            if user == request.user:
                user_data.append(UserProfileSerializer(user).data)
            else:
                user_data.append(UserSerializer(user).data)
        return Response(user_data)


class UserProfileRetrieveAPIView(RetrieveAPIView):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.user == self.get_object():
            return UserProfileSerializer
        return UserSerializer


class UserProfileUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated, IsOwner)

    def get_object(self):
        return self.request.user


class UserProfileDestroyAPIView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated, IsOwner)

    def get_object(self):
        return self.request.user


class PaymentListAPIView(ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_type')
    ordering_fields = ('payment_date',)

class PaymentCreateAPIView(CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        price = create_stripe_price(payment.amount)
        session_id, payment_link = create_stripe_session(price)
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()