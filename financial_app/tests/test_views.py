import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import User
from ..serializers import UserSerializer


# initialize the APIClient app
client = Client()


class GetAllUsersTest(TestCase):
    """
    Test module for GET all users
    """

    def setUp(self):
        User.objects.create(name="one", age=1, email="one@example.com")
        User.objects.create(name="two", age=2, email="two@example.com")

    def test_get_all_users(self):
        # get API response
        response = client.get(reverse("get_post_users"))
        # get data from db
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleUserTest(TestCase):
    """
    Test module for GET single user
    """

    def setUp(self):
        self.one = User.objects.create(name="one", age=1, email="one@example.com")
        self.two = User.objects.create(name="two", age=2, email="two@example.com")

    def test_get_valid_single_user(self):
        response = client.get(
            reverse("get_delete_put_user", kwargs={"pk": self.one.pk})
        )
        user = User.objects.get(pk=self.one.pk)
        serializer = UserSerializer(user)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_user(self):
        response = client.get(reverse("get_delete_put_user", kwargs={"pk": 999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewUserTest(TestCase):
    """
    Test module for inserting a new user
    """

    def setUp(self):
        self.valid_payload = {"name": "one", "email": "test1@example.com", "age": 42}
        # email is blank
        self.invalid_payload = {"name": "one", "email": "", "age": 42}

    def test_create_valid_user(self):
        response = client.post(
            reverse("get_post_users"),
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_user(self):
        response = client.post(
            reverse("get_post_users"),
            data=json.dumps(self.invalid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
