import uuid
from decimal import Decimal
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pin = models.CharField(max_length=10, null=False, blank=False)
    phone_number = models.CharField(max_length=10, null=False, blank=False)
    pass

    def __str__(self) -> str:
        return self.username

class Car(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    brand = models.CharField(max_length=100, null=False, blank=False)
    model = models.CharField(max_length=100, null=False, blank=False)
    year = models.DateField(null=False, blank=False)
    seats = models.IntegerField(null=False, blank=False)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))], null=False, blank=False)

    def __str__(self) -> str:
        return f"{self.brand} {self.model} {self.year}"

class Application(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f"{self.car} - {self.user}"
