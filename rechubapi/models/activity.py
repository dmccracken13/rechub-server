from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User

class Activity(models.Model):

    name = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE,)

    class Meta:
        verbose_name = ("activity")
        verbose_name_plural = ("activities")