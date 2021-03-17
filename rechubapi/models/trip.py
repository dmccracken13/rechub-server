from django.db import models
from django.db.models.deletion import DO_NOTHING, CASCADE
from rechubapi.models import Activity
from rechubapi.models import Container
from django.contrib.auth.models import User



class Trip(models.Model):
    location = models.CharField(max_length=25)
    activity = models.ForeignKey(Activity, on_delete=models.DO_NOTHING,)
    date = models.DateField(auto_now=False, auto_now_add=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE,)


    class Meta:
        verbose_name = ("trip")
        verbose_name_plural = ("trips")