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


class GetUserAccountSummaryTest(TestCase):
    """
    Test module for user_account_summary mathod
    """

    def setUp(self):
        self.user = User.objects.create(name="user", age=18, email="user@example.com")
        self.tx1 = Transaction.objects.create(
            reference="000051",
            account="C00099",
            date="2001-01-03",
            amount=-10,
            type="outflow",
            category="groceries",
            user_id=self.user.pk,
        )
        self.tx2 = Transaction.objects.create(
            reference="000052",
            account="C00099",
            date="2002-01-10",
            amount=-10,
            type="outflow",
            category="salary",
            user_id=self.user.pk,
        )
        self.tx3 = Transaction.objects.create(
            reference="000053",
            account="C00099",
            date="2003-01-10",
            amount=10,
            type="inflow",
            category="salary",
            user_id=self.user.pk,
        )

        self.tx4 = Transaction.objects.create(
            reference="000054",
            account="C00099",
            date="2004-01-10",
            amount=10,
            type="inflow",
            category="salary",
            user_id=self.user.pk,
        )

    def test_get_user_account_summary(self):

        self.assertEquals(Transaction.objects.count(), 4)

        # Invalid dates, give me all
        user_account_summary = self.user.get_user_account_summary(
            "not a date", "not a date"
        )
        dict = user_account_summary[0]
        balance = dict["balance"]
        self.assertEquals(0, balance)

        # Valid dates, but give me all
        user_account_summary = self.user.get_user_account_summary(
            "01-01-2000", "01-01-2020"
        )
        dict = user_account_summary[0]
        balance = dict["balance"]
        self.assertEquals(0, balance)

        # Valid dates, but give me one
        user_account_summary = self.user.get_user_account_summary(
            "01-01-2000", "31-12-2001"
        )
        dict = user_account_summary[0]
        balance = dict["balance"]
        self.assertEquals(-10.0, balance)


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
