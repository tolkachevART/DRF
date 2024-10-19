from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from nullable import NULLABLE


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
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
