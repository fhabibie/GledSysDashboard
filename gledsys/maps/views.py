from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from modules.chart import get_lightning_bar_chart, get_lightning_pie_chart, get_lightning_pie_chart_plotly, get_lightning_bar_chart_plotly
from modules.map import get_distribution_map
from uploads.models import Lightning
from django.utils.timezone import make_aware
from django.utils.dateparse import parse_datetime


# Create your views here.

def lighning_distribution_maps(request):
    query = Lightning.objects.filter(
            datetime_utc__range = ["2021-02-01T19:16:54+07:00", "2021-02-02T19:16:54+07:00"],
            latitude__range = [-6.34232915063942, 1.3138862223887],
            longitude__range = [94.0034031691933, 95.2507765200479],
            type__in = [0,1,2]).values_list("datetime_utc", "latitude", "longitude", "type")
    print(len(query))
    
    dist_map = get_distribution_map(query)
    context = {
        "page_title": "Lightning Distribution Maps",
        "map": "data:image/png;base64, " + dist_map
    }
    
    return render(request, 'lightning_distribution.html', context)


def lighning_temporal_chart(request):
    # Initial Dataset
    # from django.contrib.gis.geos import Polygon

    # bbox = (-6.9145,53.5958,-5.6085,53.1023)#min_lat,max_lat,min_lng,max_lng 
    # geom = Polygon.from_bbox(bbox)

    # Location.objects.filter(point__within=geom)
    
    
    query = Lightning.objects.filter(
            datetime_utc__range = ["2020-09-16T19:16:54+07:00", "2021-09-16T19:16:54+07:00"],
            latitude__range = [-6.34232915063942, 1.3138862223887],
            longitude__range = [94.0034031691933, 95.2507765200479],
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

def get_lightning_temporal_chart(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == "POST":
        ctype = request.POST.getlist('ctype[]')
        lat_range = request.POST.getlist('latRange[]')
        lon_range = request.POST.getlist('lonRange[]')
        date_range = request.POST.getlist('dateRange[]')

        query = Lightning.objects.filter(
            datetime_utc__range = date_range,
            latitude__range = lat_range,
            longitude__range = lon_range,
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