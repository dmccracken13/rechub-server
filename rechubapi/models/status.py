from django.db import models

class Status(models.Model):

    name = models.CharField(max_length=25)

    class Meta:
        verbose_name = ("status")
        verbose_name_plural = ("statuses")