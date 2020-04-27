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
