from django.core.management import BaseCommand

from materials.models import Course, Lesson
from users.models import Payment, User


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        self.create_users()
        self.create_courses()
        self.create_lessons()
        self.create_payments()
        self.stdout.write(self.style.SUCCESS("База данных успешно заполнена!"))

    def create_users(self):
        self.user1 = User.objects.create(email="user1@gmail.com", password="password1")
        self.user2 = User.objects.create(email="user2@gmail.com", password="password2")

    def create_courses(self):
        self.course1 = Course.objects.create(
            name="Международное право", description="..."
        )
        self.course2 = Course.objects.create(
            name="Гражданское право", description="---"
        )

    def create_lessons(self):
        self.lesson1 = Lesson.objects.create(
            name="Правовые отношения",
            description="туда сюда",
            video_link="https://example.com/lesson1",
        )
        self.lesson2 = Lesson.objects.create(
            name="Неправовые отношения",
            description="ни туда ни сюда",
            video_link="https://example.com/lesson2",
        )

    def create_payments(self):
        self.payment1 = Payment.objects.create(
            user=self.user1,
            paid_course=self.course1,
            paid_lesson=self.lesson1,
            amount=20000.00,
            payment_type="bank_transfer",
        )
        self.payment2 = Payment.objects.create(
            user=self.user2,
            paid_course=self.course2,
            amount=30000.00,
            payment_type="cash",
        )
