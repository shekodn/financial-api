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
        try:
            start_date_obj = datetime.datetime.strptime(start_date, "%d-%m-%Y").date()
            end_date_obj = datetime.datetime.strptime(end_date, "%d-%m-%Y").date()

        except:
            start_date_obj = datetime.date(datetime.MINYEAR, 1, 1)
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
        return self.transactions.filter(type="inflow")

    def get_user_summary_by_outflow(self):
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

    def save(self, *args, **kwargs):
        """
        Overrides default save method in order to make sure that:
            - inflows are always >= 0
            - outflows are always < 0
        """
        if self.amount >= 0:
            self.type = "inflow"
        else:
            self.type = "outflow"
        super(Transaction, self).save(*args, **kwargs)
