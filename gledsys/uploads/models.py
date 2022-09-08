from django.db import models

# Create your models here.

class LightningFiles(models.Model):
    filename = models.CharField(max_length=255)
    files = models.FileField(upload_to="csv", null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File: {self.filename}"

class Lightning(models.Model):
    datetime_utc = models.TimeField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    type = models.IntegerField()