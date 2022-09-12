from django.urls import path
from . import views

urlpatterns = [
    path('lightning-distribution/', views.lighning_distribution_maps, name="lightning-distribution")
]
