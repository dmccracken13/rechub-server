from django.db import models

class Container(models.Model):

    name = models.CharField(max_length=30)

    class Meta:
        verbose_name = ("container")
        verbose_name_plural = ("containers")