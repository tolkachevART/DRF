from django.views.generic import UpdateView

from users.models import User
from users.serializers import UserSerializer


class UserProfileUpdateAPIView(UpdateView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
