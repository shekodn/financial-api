from django.test import TestCase
from ..models import User, Transaction
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


class TransactionTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(name="user", age=18, email="user@example.com")
        self.tx1 = Transaction.objects.create(
            reference="001",
            account="S00099",
            date="2020-01-13",
            amount=100.21,
            type="inflow",
            category="salary",
            user=self.user,
        )

    def test_transaction(self):
        self.assertEquals(Transaction.objects.count(), 1)

    def test_transaction_reference_should_be_unique(self):
        self.assertEquals(Transaction.objects.count(), 1)

        try:
            with transaction.atomic():
                Transaction.objects.create(
                    reference=self.tx1.reference,
                    account="S00099",
                    date="2020-01-13",
                    amount=100.21,
                    type="inflow",
                    category="salary",
                    user=self.user,
                )
                self.fail("Duplicate reference allowed")
        except IntegrityError:
            pass

        self.assertEquals(User.objects.count(), 1)

    def test_transaction_type(self):
        """
        Make sure that the type is linked to the amount.
            - inflow is always >= 0
            - outflow is always < 0
        """

        self.tx = Transaction.objects.create(
            reference="002",
            account="S00099",
            date="2020-01-13",
            amount=-42,
            type="this makes no sense",
            category="salary",
            user=self.user,
        )

        self.assertEquals(self.tx.type, "outflow")

        self.tx = Transaction.objects.create(
            reference="003",
            account="S00099",
            date="2020-01-13",
            amount=42,
            type="this makes no sense (again)",
            category="salary",
            user=self.user,
        )

        self.assertEquals(self.tx.type, "inflow")
