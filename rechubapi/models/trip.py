from django.db import models
from django.db.models.deletion import DO_NOTHING
from rechubapi.models import Activity
from rechubapi.models import Container


class Trip(models.Model):

    name = models.CharField(max_length=25)
    activity = models.ForeignKey(Activity, on_delete=models.DO_NOTHING,)
    container = models.ForeignKey(Container, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = ("trip")
        verbose_name_plural = ("trips")