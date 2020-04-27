from django.test import TestCase
from ..models import User
from django.db.utils import IntegrityError
from django.db import transaction


class UserTestCase(TestCase):
    """ Test module for User model """

    def test_user(self):
        self.assertEquals(User.objects.count(), 0)
        User.objects.create(name="user", age=42, email="user@example.com")
        self.assertEquals(User.objects.count(), 1)

    def test_user_email_should_be_unique(self):

        self.assertEquals(User.objects.count(), 0)

        duplicated_email = "user@example.com"
        User.objects.create(name="user", age=42, email=duplicated_email)

        try:
            with transaction.atomic():
                User.objects.create(name="user", age=42, email=duplicated_email)
                self.fail("Duplicate email allowed")
        except IntegrityError:
            pass

        self.assertEquals(User.objects.count(), 1)
