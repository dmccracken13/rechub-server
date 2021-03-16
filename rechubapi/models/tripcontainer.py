from django.db import models
from django.db.models.deletion import CASCADE
from rechubapi.models import Container
from rechubapi.models import Trip


class TripContainer(models.Model):

    name = models.CharField(max_length=30)
    container = models.ForeignKey(Container, on_delete=models.CASCADE,)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE,)

    class Meta:
        verbose_name = ("tripcontainer")
        verbose_name_plural = ("tripcontainers")