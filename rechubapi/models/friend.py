from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User
from django.db import models


class Friend(models.Model):

    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friends")
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="users")

    class Meta:
        verbose_name = ("friend")
        verbose_name_plural = ("friends")