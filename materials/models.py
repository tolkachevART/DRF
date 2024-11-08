from django.conf import settings
from django.db import models

from nullable import NULLABLE


class Course(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название курса")
    preview = models.ImageField(
        upload_to="course_preview/", **NULLABLE, verbose_name="Превью курса"
    )
    description = models.TextField(verbose_name="Описание курса")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        **NULLABLE,
        verbose_name="Владелец курса"
    )
    last_update = models.DateTimeField(auto_now=True, verbose_name="Последнее изменение")

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название урока")
    preview = models.ImageField(
        upload_to="lesson_preview/", **NULLABLE, verbose_name="Превью урока"
    )
    description = models.TextField(verbose_name="Описание урока")
    video_link = models.URLField(verbose_name="Ссылка на видео")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        **NULLABLE,
        verbose_name="Владелец урока"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Последнее изменение урока")

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ["course", "name"]

    def __str__(self):
        return self.name


class Subscription(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс")

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        unique_together = ("user", "course")
