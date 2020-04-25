from django.db import models
from martor.models import MartorField
from django.conf import settings

# Create your models here.

class QPost(models.Model):
    title = models.CharField(max_length=20)
    password = models.CharField(max_length=8)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = MartorField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    hit = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    
class QComment(models.Model):
    content = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    qpost = models.ForeignKey(QPost, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)