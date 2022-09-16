from django.urls import path
from . import views

urlpatterns = [
    path('lightning-distribution/', views.lighning_distribution_maps, name="lightning-distribution"),
    path('lightning-temporal-statistics/', views.lighning_temporal_chart, name="lightning-temporal"),
    path('api/temporal', views.get_lightning_temporal_chart, name="ajax-temporal")
]
