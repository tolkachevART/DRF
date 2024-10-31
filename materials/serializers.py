from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson, Subscription
from materials.validators import validate_url


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        extra_kwargs = {'video_link': {'validators': [validate_url]}}


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    lesson_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True, source='lesson_set')
    is_subscribed = SerializerMethodField()

    def get_lesson_count(self, obj):
        return obj.lesson_set.count()

    def get_is_subscribed(self, obj):
        user = self.context.get("request").user
        return Subscription.objects.filter(user=user, course=obj).exists()

    class Meta:
        model = Course
        fields = ("name", "description", "lesson_count", "lessons", "is_subscribed")


class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = ("user", "course")
