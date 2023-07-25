from django.db import models
from apps.user.models import User
from apps.core.models import Core
from .choices import STATUS_OCR

class Images(models.Model):
    image = models.ImageField(upload_to='media/')

# Create your models here.
class OCR(Core):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    data = models.JSONField()
    response = models.JSONField(null=True, blank=True)
    status = models.CharField(choices=STATUS_OCR, max_length=3, default='1')

    def __str__(self):
        return f'{self.created_at} - {self.id} - {self.get_status_display()} - {self.user.username}'

    class Meta:
        ordering = ['-created_at']
