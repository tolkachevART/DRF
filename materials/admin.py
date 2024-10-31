from django.contrib import admin

from materials.models import Course, Lesson, Subscription


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )
    search_fields = ("name",)
    list_filter = ("name",)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "course")
    search_fields = ("course",)
    list_filter = ("name",)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "course")
    search_fields = ("user", "course")
    list_filter = ("user", "course")
