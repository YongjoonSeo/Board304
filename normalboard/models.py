from django.db import models
from martor.models import MartorField

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=20)
    password = models.CharField(max_length=8)
    content = MartorField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)