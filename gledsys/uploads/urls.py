from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("upload-lightning/", views.upload_lightning, name="upload-lightning"),
    path("upload-lightning/<int:id_files>/", views.detail_lightning, name="detail-lightning")
]