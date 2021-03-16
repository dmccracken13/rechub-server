from django.db import models

class Type(models.Model):

    name = models.CharField(max_length=25)

    class Meta:
        verbose_name = ("type")
        verbose_name_plural = ("types")