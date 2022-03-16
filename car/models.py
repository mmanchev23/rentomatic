import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pin = models.CharField(max_length=10, null=False, blank=False)
    phone_number = models.CharField(max_length=10, null=False, blank=False)
    pass

    def __str__(self) -> str:
        return self.username
