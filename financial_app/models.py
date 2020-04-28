from django.db import models
from django.db.models import Sum, Case, When, F, DecimalField
import datetime


class User(models.Model):
    """
    User Model
    Defines the attributes of a user
    """

    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    age = models.IntegerField()

    def __str__(self):
        return f"{self.name} {self.email} {self.age}"

    def get_user_account_summary(self, start_date, end_date):
        """
        Description:
            This method filters the user's transactions in order to get a
            summary. This one shows the balance of the account,
            the sum of total inflows and total outflows. After we calculate
            the balance and return the respective account.

        Paramters:
            start_date (string):
                If we want to filter by date we need a starting date
                (eg. 12-01-2020)
            end_date (string):
                If we want to filter by date we need an end date
                (eg. 12-01-2020)
        Return:
            A dictionary containing the user_account_summary (total_inflow,
            total_outflow, balance and account)

        """

        # Tries to get start_date, because end_date might not be present or valid
        try:
            start_date_obj = datetime.datetime.strptime(start_date, "%d-%m-%Y").date()
        except:
            start_date_obj = datetime.date(datetime.MINYEAR, 1, 1)

        # Tries to get end_date, because start_date might not be present or valid
        try:
            end_date_obj = datetime.datetime.strptime(end_date, "%d-%m-%Y").date()
        except:
            end_date_obj = datetime.date(datetime.MAXYEAR, 12, 31)

        return (
            self.transactions.filter(date__range=[start_date_obj, end_date_obj])
            .values("account")
            .annotate(
                total_inflow=Sum(
                    Case(
                        When(type="inflow", then=F("amount")),
                        output_field=DecimalField(),
                        default=0,
                    )
                ),
                total_outflow=Sum(
                    Case(
                        When(type="outflow", then=F("amount")),
                        output_field=DecimalField(),
                        default=0,
                    )
                ),
                balance=F("total_inflow") + F("total_outflow"),
            )
        )

    def get_user_summary_by_inflow(self,):
        """
        Description
            We need to filter our data by category/type. So here we filter
            by inflow type.
        Return:
            A dictionary containing the transactions filtered by inflow
        """
        return self.transactions.filter(type="inflow")

    def get_user_summary_by_outflow(self):
        """
        Description
            We need to filter our data by category/type. So here we filter
            by outflow type.
        Return:
            A dictionary containing the transactions filtered by outflow
        """
        return self.transactions.filter(type="outflow")


class Transaction(models.Model):
    """
    Transaction Model
    Defines the attributes of a transaction
    """

    reference = models.CharField(max_length=30, unique=True)
    account = models.CharField(max_length=30)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=10)
    category = models.CharField(max_length=50)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="transactions"
    )

    def __str__(self):
        return f"{self.reference} {self.account} {self.date} {self.amount} {self.type} {self.category} {self.user}"

    def __get_type(self):
        """
        Description:
            Determines type based on amount.
                - inflows are always >= 0
                - outflows are always < 0
        """
        if self.amount >= 0:
            self.type = "inflow"
        else:
            self.type = "outflow"

    def save(self, *args, **kwargs):
        # Used to override the default save method in order to determine the type
        # based in the transaction amount
        self.__get_type()

        super(Transaction, self).save(*args, **kwargs)
