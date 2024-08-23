from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Address(models.Model):
    user = models.ForeignKey(User, related_name='addresses', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}: {self.address}"
