from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from materials.models import Course, Lesson
from nullable import NULLABLE

PAYMENT_TYPE_CHOICES = (
    ("cash", "Наличные"),
    ("bank_transfer", "Банковский перевод"),
)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, help_text="Укажите вашу почту")
    phone = PhoneNumberField(
        verbose_name="Телефон", **NULLABLE, help_text="Введите номер телефона"
    )
    city = models.CharField(
        max_length=50, verbose_name="Город", **NULLABLE, help_text="Введите ваш город"
    )
    avatar = models.ImageField(
        upload_to="users_avatars/",
        verbose_name="Аватар",
        **NULLABLE,
        help_text="Загрузите изображение"
    )
    token = models.CharField(max_length=100, verbose_name="Token", **NULLABLE)
    last_login = models.DateTimeField(auto_now_add=True, **NULLABLE, verbose_name="Последний вход в аккаунт")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    payment_date = models.DateField(auto_now_add=True, verbose_name="Дата оплаты")
    paid_course = models.ManyToManyField(
        Course, blank=True, verbose_name="Оплаченный курс", related_name="payments"
    )
    paid_lesson = models.ManyToManyField(
        Lesson, blank=True, verbose_name="Оплаченный урок", related_name="payments"
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Сумма оплаты"
    )
    payment_type = models.CharField(
        max_length=50, verbose_name="Способ оплаты", choices=PAYMENT_TYPE_CHOICES
    )
    session_id = models.CharField(max_length=255, verbose_name="ID сессии в Stripe", **NULLABLE)
    link = models.URLField(max_length=400, verbose_name="Ссылка на оплату", **NULLABLE)

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return f"{self.user} - {self.amount}"
