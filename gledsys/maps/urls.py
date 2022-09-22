from django.urls import path
from . import views

urlpatterns = [
    path('lightning-distribution/', views.lightning_distribution_map, name="lightning-distribution"),
    path('lightning-density/', views.lightning_density_map, name="lightning-density"),
    path('lightning-spatial-statistics/', views.lightning_spatial_chart, name="lightning-spatial"),
    path('lightning-temporal-statistics/', views.lightning_temporal_chart, name="lightning-temporal"),
    path('api/distribution', views.ajax_lightning_distribution_map, name="ajax-distribution"),
    path('api/density', views.ajax_lightning_density_map, name="ajax-density"),
    path('api/temporal', views.ajax_lightning_temporal_chart, name="ajax-temporal"),
    path('api/spatial', views.ajax_lightning_spatial, name="ajax-spatial")
]
