from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from modules.chart import get_lightning_bar_chart, get_lightning_pie_chart, get_lightning_pie_chart_plotly, get_lightning_bar_chart_plotly
from uploads.models import Lightning
from django.utils.timezone import make_aware
from django.utils.dateparse import parse_datetime


# Create your views here.

def lighning_distribution_maps(request):
    context = {
        "page_title": "Lightning Distribution Maps",
    }
    
    return render(request, 'lightning_distribution.html', context)


def lighning_temporal_chart(request):

    # chart = get_lightning_bar_chart()
    # Get initial chart
    query = Lightning.objects.filter(
            datetime_utc__range = ["2020-09-16T19:16:54+07:00", "2021-09-16T19:16:54+07:00"],
            latitude__range = [-6.34232915063942, 1.3138862223887],
            longitude__range = [94.0034031691933, 95.2507765200479],
            type__in = [0,1,2]).values_list("datetime_utc", "type")

    print('query len', len(query))
    if len(query) > 0:
        bar_chart = get_lightning_bar_chart(query)
        bar_chart = "data:image/png;base64, " + bar_chart
        pie_chart = get_lightning_pie_chart(query)
        pie_chart = "data:image/png;base64, " + pie_chart
        pie_plotly = get_lightning_pie_chart_plotly(query)
        bar_plotly = get_lightning_bar_chart_plotly(query)

    else:
        # Add default img
        bar_chart = ''
        pie_chart = ''
        pie_plotly = ''
        bar_plotly = ''

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