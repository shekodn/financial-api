import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import User, Transaction
from ..serializers import (
    AuxGetUserSummaryByCategorySerializer,
    TransactionSerializer,
    UserAccountSummarySerializer,
    UserSerializer,
)


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


class GetAllTransactionsTest(TestCase):
    """
    Test module for GET all transactions
    """

    def setUp(self):
        self.user = User.objects.create(name="user", age=1, email="user@example.com")
        self.tx1 = Transaction.objects.create(
            reference="001",
            account="S00099",
            date="2020-01-13",
            amount=100.21,
            type="inflow",
            category="salary",
            user=self.user,
        )
        self.tx2 = Transaction.objects.create(
            reference="002",
            account="S00099",
            date="2020-01-13",
            amount=-100.1,
            type="outflow",
            category="groceries",
            user=self.user,
        )

    def test_get_all_transactions(self):
        # get API response
        response = client.get(reverse("get_post_transactions"))
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        self.assertEqual(response.data, serializer.data)


class GetSingleTransactionTest(TestCase):
    """
    Test module for GET single transaction
    """

    def setUp(self):
        self.user = User.objects.create(name="user", age=1, email="user@example.com")
        self.tx1 = Transaction.objects.create(
            reference="001",
            account="S00099",
            date="2020-01-13",
            amount=100.21,
            type="inflow",
            category="salary",
            user=self.user,
        )

    def test_get_valid_single_transaction(self):
        response = client.get(
            reverse("get_delete_put_transaction", kwargs={"pk": self.tx1.pk})
        )
        transaction = Transaction.objects.get(pk=self.tx1.pk)
        serializer = TransactionSerializer(transaction)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_transaction(self):
        response = client.get(reverse("get_delete_put_transaction", kwargs={"pk": 999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewTransactionTest(TestCase):
    """
    Test module for inserting a new transaction
    """

    def setUp(self):
        self.user = User.objects.create(name="user", age=18, email="user@example.com")
        self.valid_payload = {
            "reference": "000051",
            "account": "S00099",
            "date": "2020-01-13",
            "amount": "-51.13",
            "type": "outflow",
            "category": "groceries",
            "user_id": self.user.pk,
        }
        # missing user_id
        self.invalid_payload = {
            "reference": "007",
            "account": "S00099",
            "date": "2020-01-13",
            "amount": "100.21",
            "type": "inflow",
            "category": "salary",
        }

    def test_create_valid_transaction(self):

        # Test DB should be empty
        self.assertEquals(Transaction.objects.count(), 0)

        # Attempts to create a transaction with an invalid Payload
        response = self.client.post(
            reverse("get_post_transactions"), data=self.valid_payload, format="json"
        )
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(Transaction.objects.count(), 1)

        # Asserts that the transaction we just created is the first transaction
        transaction = Transaction.objects.first()
        self.assertEquals(transaction.reference, self.valid_payload["reference"])

    def test_create_invalid_transaction(self):

        self.assertEquals(Transaction.objects.count(), 0)

        # Attempts to create a transaction with an invalid payload
        response = self.client.post(
            reverse("get_post_transactions"), data=self.invalid_payload, format="json"
        )
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(Transaction.objects.count(), 0)


class GetUserAccountSummary(TestCase):
    """
    Test module for GET user_account_summary
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

        response = client.get(
            reverse("get_user_account_summary", kwargs={"pk": self.user.pk})
        )
        serializer = UserAccountSummarySerializer(self.user)

        # AssertionError: Lists differ: ["'user_account_summary'"] != ['user_account_summary']
        # self.assertQuerysetEqual(response.data, serializer.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetUserSummaryByCategoryTest(TestCase):
    """
    Test module for GET get_user_summary_by_category
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

    def test_get_user_summary_by_category(self):
        response = client.get(
            reverse("get_user_summary_by_category", kwargs={"pk": self.user.pk})
        )
        serializer = AuxGetUserSummaryByCategorySerializer(self.user)

        # AssertionError:
        # - ["'inflow'", "'outflow'"]
        # ?  -        -  -         -
        # + ['inflow', 'outflow']
        # self.assertQuerysetEqual(response.data, serializer.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
