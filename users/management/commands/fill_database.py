import random

from django.contrib.auth.hashers import make_password
from django.core.management import BaseCommand

from materials.models import Course, Lesson
from users.models import Payment, User


class Command(BaseCommand):
    help = "Заполняет базу данных пользователями, курсами, уроками и платежами."

    def add_arguments(self, parser):
        parser.add_argument(
            '--seed', type=int, default=1, help='Количество случайных записей.'
        )

    def handle(self, *args, seed=1, **options):
        self.stdout.write(self.style.NOTICE("Заполнение базы данных..."))
        self.create_users(seed)
        self.create_courses(seed)
        self.create_lessons(seed)
        self.create_payments(seed)
        self.stdout.write(self.style.SUCCESS("База данных успешно заполнена!"))

    def create_users(self, count):
        for _ in range(count):
            user = User.objects.create(
                email=f"user{random.randint(1, 99)}@gmail.com",
                password=make_password("<PASSWORD>"),
            )
            self.stdout.write(self.style.SUCCESS(f"Создание пользователя: {user}"))

    def create_courses(self, count):
        for _ in range(count):
            course = Course.objects.create(
                name=f"Курс {random.randint(1, 99)}",
                description=f"Краткое описание курса {random.randint(1, 99)}",
            )
            self.stdout.write(self.style.SUCCESS(f"Создание курса: {course}"))

    def create_lessons(self, count):
        courses = Course.objects.all()
        for _ in range(count):
            lesson = Lesson.objects.create(
                name=f"Урок {random.randint(1, 99)}",
                description=f"Описание урока {random.randint(1, 99)}",
                video_link=f"https://example.com/lesson_{random.randint(1, 99)}",
                course=random.choice(courses),
            )
            self.stdout.write(self.style.SUCCESS(f"Создание урока: {lesson}"))

    def create_payments(self, count):
        for _ in range(count):
            user = User.objects.get(pk=random.randint(1, 99))
            course = Course.objects.get(pk=random.randint(1, 99))
            lesson = Lesson.objects.get(pk=random.randint(1, 99))
            payment = Payment.objects.create(
                user=user,
                paid_course=course,
                paid_lesson=lesson,
                amount=10000.00,
                payment_type="bank_transfer",
            )
            self.stdout.write(self.style.SUCCESS(f"Создание платежа: {payment}"))
