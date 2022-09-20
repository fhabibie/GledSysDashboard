from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from modules.chart import get_lightning_bar_chart, get_lightning_pie_chart, get_lightning_pie_chart_plotly, get_lightning_bar_chart_plotly
from modules.map import get_distribution_map, create_geojson
from uploads.models import Lightning
from django.contrib.gis.gdal.envelope import Envelope
from django.contrib.gis.geos import Polygon, Point
from django.utils.timezone import make_aware
from django.utils.dateparse import parse_datetime
from django.core.serializers import serialize
import json


# Create your views here.

def lightning_distribution_map(request):
    # Returns a polygon object from the given bounding-box, a 4-tuple comprising (xmin, ymin, xmax, ymax).
    # coord_range = (94, -12, 144, 10)
    coord_range = (100, -1, 108, 7)
    boundary_box = Polygon.from_bbox(coord_range)
    
    query = Lightning.objects.filter(
            datetime_utc__range = ["2021-02-01T19:16:54+07:00", "2021-02-05T19:16:54+07:00"],
            coord__within = boundary_box,
            type__in = [0,1,2]).values_list("datetime_utc", "latitude", "longitude", "type")
    print(len(query))

    dist_map = ""
    if len(query) > 0:
        dist_map = get_distribution_map(query, coord_range)
    context = {
        "page_title": "Lightning Distribution Maps",
        "map": "data:image/png;base64, " + dist_map
    }
    
    return render(request, 'lightning_distribution.html', context)

def ajax_lightning_distribution_map(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == "POST":
        ctype = request.POST.getlist('ctype[]')
        lat_range = request.POST.getlist('latRange[]')
        lon_range = request.POST.getlist('lonRange[]')
        date_range = request.POST.getlist('dateRange[]')
        
        coord_range = (float(lon_range[0]), float(lat_range[0]), float(lon_range[1]), float(lat_range[1]))
        print('coord',coord_range)

        boundary_box = Polygon.from_bbox(coord_range)

        query = Lightning.objects.filter(
            datetime_utc__range = date_range,
            coord__within = boundary_box,
            type__in = [0,1,2])
        query_map = query.values_list("datetime_utc", "latitude", "longitude", "type")
        geojson = {}
        dist_map = ""
        if len(query) > 0:
            dist_map = get_distribution_map(query_map, coord_range)
            geojson = serialize('geojson', query, geometry_field='coord', fields=('type', 'datetime_utc'))
            return JsonResponse({"success":True, "data": {"map": "data:image/png;base64, " + dist_map, "geojson": geojson}}, status = 200)
        else:
            return JsonResponse({"success": True,}, status = 200)

        
    return JsonResponse({"success": False}, status=400)



def lightning_temporal_chart(request):
    # coord_range = (94, -12, 144, 10)
    coord_range = (100, -1, 108, 7)
    boundary_box = Polygon.from_bbox(coord_range)
    
    query = Lightning.objects.filter(
            datetime_utc__range = ["2021-02-01T19:16:54+07:00", "2021-02-05T19:16:54+07:00"],
            coord__within = boundary_box,
            type__in = [0,1,2]).values_list("datetime_utc", "type")

    bar_chart, pie_chart, bar_plotly, pie_plotly = "", "", "", ""

    if len(query) > 0:
        bar_chart = get_lightning_bar_chart(query)
        bar_chart = "data:image/png;base64, " + bar_chart
        pie_chart = get_lightning_pie_chart(query)
        pie_chart = "data:image/png;base64, " + pie_chart
        pie_plotly = get_lightning_pie_chart_plotly(query)
        bar_plotly = get_lightning_bar_chart_plotly(query)


    context = {
        "page_title": "Lightning Temporal Statistics",
        "bar_chart": bar_chart,
        "pie_chart": pie_chart,
        "pie_plotly": pie_plotly,
        "bar_plotly": bar_plotly,
    }
    return render(request, 'lightning_temporal.html', context)

def ajax_lightning_temporal_chart(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == "POST":
        ctype = request.POST.getlist('ctype[]')
        lat_range = request.POST.getlist('latRange[]')
        lon_range = request.POST.getlist('lonRange[]')
        date_range = request.POST.getlist('dateRange[]')
        
        boundary_box = Polygon.from_bbox((lon_range[0], lat_range[0], lon_range[1], lat_range[1]))

        query = Lightning.objects.filter(
            datetime_utc__range = date_range,
            coord__within = boundary_box,
            type__in = ctype,
            ).values_list("datetime_utc", "type")

        if len(query) > 0:
            bar_chart = get_lightning_bar_chart(query)
            bar_chart = "data:image/png;base64, " + bar_chart
            pie_chart = get_lightning_pie_chart(query)
            pie_chart = "data:image/png;base64, " + pie_chart

            pie_plotly = get_lightning_pie_chart_plotly(query)
            bar_plotly = get_lightning_bar_chart_plotly(query)

            return JsonResponse({"success":True, "data": {"bar": bar_chart, "pie": pie_chart, "pieplotly": pie_plotly, "barplotly": bar_plotly}}, status = 200)
        else:
            return JsonResponse({"success": True,}, status = 200)

        
    return JsonResponse({"success": False}, status=400)