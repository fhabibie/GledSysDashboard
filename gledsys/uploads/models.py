# from django.db import models
from django.contrib.gis.db import models

# Create your models here.

class LightningFiles(models.Model):
    filename = models.CharField(max_length=255)
    files = models.FileField(upload_to="csv", null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File: {self.filename}"

    def path(self):
        return self.files.path

class Lightning(models.Model):
    files = models.ForeignKey(LightningFiles, on_delete=models.CASCADE)
    datetime_utc = models.DateTimeField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    coord = models.PointField()
    type = models.IntegerField()


class SavedShapefile(models.Model):
    filename = models.CharField(max_length=255)
    shp_file = models.FileField(upload_to="shp", null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File: {self.filename}"

    def path(self):
        return self.shp_file.path