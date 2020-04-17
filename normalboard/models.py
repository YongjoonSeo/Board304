from django.db import models
from martor.models import MartorField
from django.conf import settings

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=20)
    password = models.CharField(max_length=8)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = MartorField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

