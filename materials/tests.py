from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):
    def setUp(self):
        self.group = Group.objects.create(name="moders")
        self.moder = User.objects.create(email="moder@mail.com", password="modertest")
        self.moder.groups.add(self.group)
        self.user = User.objects.create(email="test@mail.com", password="test")
        self.user2 = User.objects.create(email="test2@mail.com", password="test2")
        self.course = Course.objects.create(name="Test course", description="Test course description")
        self.lesson = Lesson.objects.create(name="Test lesson", description="Test lesson description",
                                            video_link="https://www.youtube.com/watch?v=gomhMmutBs0",
                                            course=self.course,
                                            owner=self.user)
        self.lesson2 = Lesson.objects.create(name="Test lesson 2", description="Test lesson description 2",
                                             video_link="https://www.youtube.com/watch?v=gomhMmutBs2",
                                             course=self.course,
                                             owner=self.user2)
        self.client.force_authenticate(user=self.user)

    def test_list_lesson(self):
        url = reverse("materials:lesson_list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "name": self.lesson.name,
                    "preview": self.lesson.preview,
                    "description": self.lesson.description,
                    "video_link": self.lesson.video_link,
                    "course": self.course.pk,
                    "owner": self.user.pk
                },
            ]
        }
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data, result
        )

    def test_retrieve_lesson(self):
        url = reverse("materials:lesson_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("name"), self.lesson.name
        )
        url = reverse("materials:lesson_retrieve", args=(self.lesson2.pk,))
        response = self.client.get(url)
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN
        )

    def test_create_lesson(self):
        url = reverse("materials:lesson_create")
        data = {
            "name": "New test lesson",
            "description": "New test lesson description",
            "video_link": "https://www.youtube.com/watch?v=gomhMmutBd9",
            "course": self.course.pk
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Lesson.objects.all().count(), 3
        )

    def test_update_lesson(self):
        url = reverse("materials:lesson_update", args=(self.lesson.pk,))
        data = {
            "name": "Updated test lesson",
            "description": "Updated test lesson description",
            "video_link": "https://www.youtube.com/watch?v=gomhMmutBd10",
            "course": self.course.pk
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "Updated test lesson")

        url = reverse("materials:lesson_update", args=(self.lesson2.pk,))
        response = self.client.put(url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_lesson(self):
        url = reverse("materials:lesson_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Lesson.objects.all().count(), 1
        )
        url = reverse("materials:lesson_delete", args=(self.lesson2.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN
        )

    def test_moder_can_update_lesson(self):
        self.client.force_authenticate(user=self.moder)
        url = reverse("materials:lesson_update", args=(self.lesson.pk,))
        data = {
            "name": "Moder updated test lesson",
            "description": "Moder updated test lesson description",
            "video_link": "https://www.youtube.com/watch?v=gomhMmutBd11",
            "course": self.course.pk
        }
        response = self.client.put(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("name"), "Moder updated test lesson"
        )

    def test_moder_cannot_delete_lesson(self):
        self.client.force_authenticate(user=self.moder)
        url = reverse("materials:lesson_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN
        )


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@mail.com", password="test")
        self.course = Course.objects.create(name="Test course", description="Test course description")
        self.client.force_authenticate(user=self.user)

    def test_subscription(self):
        # Создание подписки
        url = reverse("materials:subscription")
        data = {"course_id": self.course.pk,
                "user": self.user.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Подписка добавлена", response.data["message"])
