from django.db import models
from django.contrib.auth.models import User

class Activity(models.Model):

    name = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING,)

    class Meta:
        verbose_name = ("activity")
        verbose_name_plural = ("activities")