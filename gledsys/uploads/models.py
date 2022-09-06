from django.db import models

# Create your models here.
class lightning(models.Model):
    datetime = models.TimeField()
    lat = models.FloatField()
    long = models.FloatField()
    type = models.IntegerField()