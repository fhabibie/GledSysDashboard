from django.contrib import admin
from .models import LightningFiles, Lightning, SavedShapefile

# Register your models here.

admin.site.register(LightningFiles)
admin.site.register(Lightning)
admin.site.register(SavedShapefile)
