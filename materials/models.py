from django.db import models

from nullable import NULLABLE


class Course(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название курса")
    preview = models.ImageField(
        upload_to="course_preview/", **NULLABLE, verbose_name="Превью курса"
    )
    description = models.TextField(verbose_name="Описание курса")

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

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ["course", "name"]

    def __str__(self):
        return self.name
