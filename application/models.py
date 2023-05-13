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


class ProfileEntries(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, default = None)
    sadness = models.FloatField(default=(100/6))
    joy = models.FloatField(default=(100/6))
    surpise = models.FloatField(default=(100/6))
    love = models.FloatField(default=(100/6))
    anger = models.FloatField(default=(100/6))
    fear = models.FloatField(default=(100/6))
    text = models.CharField(max_length=1000, blank=True, null=True)
    submitted_at = models.DateField(auto_now_add=True)

    def str(self):
        return self.user.username

class ProfileMood(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    happy_songs = models.FloatField(default=3)
    sad_songs = models.FloatField(default=2)
    calm_songs = models.FloatField(default=2)
    energetic_songs = models.FloatField(default=3)

    def str(self):
        return self.user.username


class CustomProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=10, null=True)
    last_name = models.CharField(max_length=10, null=True)
    email = models.EmailField(max_length=100, null=True)
    contact = models.CharField(max_length=15, null=True)
    gender = models.CharField(max_length=10, null=True)
    age = models.IntegerField(null=True)
    music = models.CharField(max_length=100,default='1999')
    def str(self):
        return self.user.username