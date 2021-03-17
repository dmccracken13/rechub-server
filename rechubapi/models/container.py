from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User


class Container(models.Model):

    name = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE,)

    class Meta:
        verbose_name = ("container")
        verbose_name_plural = ("containers")