from django.urls import path
from . import views

urlpatterns = [
    path('lightning-distribution/', views.lightning_distribution_map, name="lightning-distribution"),
    path('lightning-temporal-statistics/', views.lightning_temporal_chart, name="lightning-temporal"),
    path('api/temporal', views.ajax_lightning_temporal_chart, name="ajax-temporal")
]
