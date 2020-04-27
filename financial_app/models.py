from django.db import models


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
