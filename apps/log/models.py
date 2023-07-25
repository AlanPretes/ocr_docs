from django.db import models
from apps.user.models import User
from apps.core.models import Core


class Log(Core):
    user = models.CharField(max_length=255)
    rota = models.CharField(max_length=255)
    ip = models.CharField(max_length=255)
    latitude = models.CharField(max_length=255, blank=True, null=True)
    longitude = models.CharField(max_length=255, blank=True, null=True)
    metodo = models.CharField(max_length=10)
    content = models.JSONField()

    def __str__(self):
        return f'{self.created_at} - {self.id} - {self.ip} - {self.user}'

    class Meta:
        ordering = ['-created_at']
