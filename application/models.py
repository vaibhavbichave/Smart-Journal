from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    sadness = models.FloatField(default=(100/6))
    joy = models.FloatField(default=(100/6))
    surpise = models.FloatField(default=(100/6))
    love = models.FloatField(default=(100/6))
    anger = models.FloatField(default=(100/6))
    fear = models.FloatField(default=(100/6))
    text = models.CharField(max_length=1000, blank=True, null=True)
    music = models.CharField(max_length=100,default='1999')

    def str(self):
        return self.user.username