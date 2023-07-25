from uuid import uuid4
from django.db import models
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    first_login = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.username = self.email
        super().save(*args, **kwargs)

        user_obj = User.objects.get(id=self.id)
        return Token.objects.get_or_create(user=user_obj)

    def __str__(self):
        return f'{self.email}'

    class Meta:
        ordering = ['email']
