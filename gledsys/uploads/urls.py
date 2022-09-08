from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("upload-lightning/", views.upload_lightning, name="upload_lightning")
]