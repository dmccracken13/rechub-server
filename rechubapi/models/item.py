from django.db.models.deletion import DO_NOTHING, CASCADE
from rechubapi.models.activity import Activity
from rechubapi.models import Status
from rechubapi.models import Container
from rechubapi.models import Type
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Item(models.Model):

    name = models.CharField(max_length=25)
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    activity = models.ForeignKey(Activity, on_delete=models.DO_NOTHING)
    container = models.ForeignKey(Container, null=True, blank=True, on_delete=models.DO_NOTHING)
    status = models.ForeignKey(Status, on_delete=models.DO_NOTHING)
    type = models.ForeignKey(Type, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        verbose_name = ("item")
        verbose_name_plural = ("items")