from celery import shared_task
from django.core.mail import send_mail

from confing.settings import EMAIL_HOST_USER
from materials.models import Subscription


@shared_task
def send_update_course_email(course_id):
    subscriptions = Subscription.objects.select_related("course").filter(course_id=course_id)
    if subscriptions:
        course = subscriptions.first().course
        send_mail(
            "Обновление курса",
            f"Курс '{course.name}' был успешно обновлен",
            from_email=EMAIL_HOST_USER,
            recipient_list=[subscription.user.email for subscription in subscriptions]
        )
