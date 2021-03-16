from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User
from rechubapi.models import Trip


class TripFriend(models.Model):

    name = models.CharField(max_length=30)
    friend = models.ForeignKey(User, on_delete=models.CASCADE,)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE,)

    class Meta:
        verbose_name = ("tripfriend")
        verbose_name_plural = ("tripfriends")