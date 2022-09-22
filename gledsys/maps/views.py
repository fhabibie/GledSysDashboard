from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from modules.chart import get_lightning_bar_chart, get_lightning_pie_chart, get_lightning_pie_chart_plotly, get_lightning_bar_chart_plotly
from modules.map import get_density_map
from uploads.models import Lightning, LightningFiles, SavedShapefile
from django.contrib.gis.gdal.envelope import Envelope
from django.contrib.gis.geos import Polygon, Point
from django.utils.timezone import make_aware
from django.utils.dateparse import parse_datetime
from django.core.serializers import serialize
import json
from django.contrib.gis.gdal import DataSource
import geopandas as gpd
import pandas as pd
from shapely import wkt
from django.contrib.gis.geos import GEOSGeometry


# Create your views here.

def lightning_distribution_map(request):
    # Returns an empty map
    context = {
        "page_title": "Lightning Distribution Maps",
    }
    
    return render(request, 'lightning_distribution.html', context)

def ajax_lightning_distribution_map(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == "POST":
        ctype = request.POST.getlist('ctype[]')
        lat_range = request.POST.getlist('latRange[]')
        lon_range = request.POST.getlist('lonRange[]')
        date_range = request.POST.getlist('dateRange[]')
        
        # Create a polygon object from the given bounding-box, a 4-tuple comprising (xmin, ymin, xmax, ymax).
        coord_range = (float(lon_range[0]), float(lat_range[0]), float(lon_range[1]), float(lat_range[1]))
        boundary_box = Polygon.from_bbox(coord_range)

        query = Lightning.objects.filter(
            datetime_utc__range = date_range,
            coord__within = boundary_box,
            type__in = ctype)
        geojson = {}
        if len(query) > 0:
            geojson = serialize('geojson', query, geometry_field='coord', fields=('type', 'datetime_utc'))
            return JsonResponse({"success":True, "data": {"geojson": geojson}}, status = 200)
        else:
            return JsonResponse({"success": True,}, status = 200)

        
    return JsonResponse({"success": False}, status=400)


def lightning_density_map(request):
    # Returns an empty map
    dist_map = get_density_map()
    context = {
        "page_title": "Lightning Density Maps",
        "map": "data:image/png;base64, " + dist_map,
    }
    
    return render(request, 'lightning_density.html', context)

def ajax_lightning_density_map(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == "POST":
        ctype = request.POST.getlist('ctype[]')
        lat_range = request.POST.getlist('latRange[]')
        lon_range = request.POST.getlist('lonRange[]')
        date_range = request.POST.getlist('dateRange[]')
        
        # Create a polygon object from the given bounding-box, a 4-tuple comprising (xmin, ymin, xmax, ymax).
        coord_range = (float(lon_range[0]), float(lat_range[0]), float(lon_range[1]), float(lat_range[1]))
        boundary_box = Polygon.from_bbox(coord_range)

        query = Lightning.objects.filter(
            datetime_utc__range = date_range,
            coord__within = boundary_box,
            type__in = ctype).values_list("datetime_utc", "latitude", "longitude", "type")
        
        dist_map = ""
        if len(query) > 0:
            dist_map = get_density_map(query, coord_range)
            return JsonResponse({"success":True, "data": {"map": "data:image/png;base64, " + dist_map}}, status = 200)
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


def lightning_spatial_chart(request):
    # Returns an empty map
    shp = SavedShapefile.objects.all()
    context = {
        "page_title": "Lightning Spatial Statistics",
        "shp_files": shp,
    }
    
    return render(request, 'lightning_spatial.html', context)

def ajax_lightning_spatial(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == "POST":
        ctype = request.POST.getlist('ctype[]')
        ctype = [int(x) for x in ctype]
        
        query_type = request.POST.getlist('queryType')[0]
        start = request.POST.getlist('start')[0]
        end = request.POST.getlist('end')[0]
        date_range = [start, end]

        if query_type == 'bbox-query':
            print('bbox-query')
            min_lat = request.POST.getlist('minLat')[0]
            max_lat = request.POST.getlist('maxLat')[0]
            min_lng = request.POST.getlist('minLng')[0]
            max_lng = request.POST.getlist('maxLng')[0]
            # Create a polygon object from the given bounding-box, a 4-tuple comprising (xmin, ymin, xmax, ymax).
            coord_range = (float(min_lng), float(min_lat), float(max_lng), float(max_lat))
            boundary_box = Polygon.from_bbox(coord_range)
            query = Lightning.objects.filter(
                datetime_utc__range = date_range,
                coord__within = boundary_box,
                type__in = ctype)
            
            print('Query on boundary box', coord_range)
            print('Result len', len(query))
            if len(query) > 0:
                points = serialize('geojson', query, geometry_field='coord', fields=('type', 'datetime_utc'))
                bar_plotly = get_lightning_bar_chart_plotly(query.values_list("datetime_utc", "type"))
                data = {
                    "points": points,
                    "polys": boundary_box.json,
                    "barplotly": bar_plotly
                }
                return JsonResponse({"success":True, "data": data}, status = 200)
            else:
                return JsonResponse({"success": True,}, status = 200)

        elif query_type == 'shp-query':
            print('SHP Query')
            shp_file = request.FILES.getlist('shp')[0]
            obj  = SavedShapefile.objects.create(filename=shp_file, shp_file= shp_file)
            print('Saved SHP', obj.filename)

            df = gpd.read_file(obj.shp_file.path)
            polys = df.to_json()

            query = Lightning.objects.filter(
                datetime_utc__range = date_range,
                type__in = ctype,
            )
            if len(query) > 0:
                query_res = None
                for index, row in df.iterrows():
                    tmp_geom = GEOSGeometry(row.geometry.wkt)
                    print('Query Geom {}/{}'.format(index+1, df.shape[0]))
                    tmp_query = query.filter(coord__within = tmp_geom)
                    if query_res == None:
                        query_res = tmp_query
                    elif len(tmp_query) > 0:
                        query_res = query_res | tmp_query

                points = serialize('geojson', query_res, geometry_field='coord', fields=('type', 'datetime_utc'))
                bar_plotly = get_lightning_bar_chart_plotly(query.values_list("datetime_utc", "type"))
                data = {
                    "points": points,
                    "polys": polys,
                    "barplotly": bar_plotly
                }
                return JsonResponse({"success":True, "data": data}, status = 200)
            else:
                return JsonResponse({"success": True,}, status = 200)

        elif query_type == 'savedshp-query':
            shp_id = request.POST.getlist('shpId')[0]
            shp = SavedShapefile.objects.get(id = shp_id)
            
            df = gpd.read_file(shp.shp_file.path)
            polys = df.to_json()

            query = Lightning.objects.filter(
                datetime_utc__range = date_range,
                type__in = ctype,
            )
            if len(query) > 0:
                query_res = None
                for index, row in df.iterrows():
                    tmp_geom = GEOSGeometry(row.geometry.wkt)
                    print('Query Geom {}/{}'.format(index+1, df.shape[0]))
                    tmp_query = query.filter(coord__within = tmp_geom)
                    if query_res == None:
                        query_res = tmp_query
                    elif len(tmp_query) > 0:
                        query_res = query_res | tmp_query

                points = serialize('geojson', query_res, geometry_field='coord', fields=('type', 'datetime_utc'))
                bar_plotly = get_lightning_bar_chart_plotly(query.values_list("datetime_utc", "type"))
                data = {
                    "points": points,
                    "polys": polys,
                    "barplotly": bar_plotly
                }
                return JsonResponse({"success":True, "data": data}, status = 200)
            else:
                return JsonResponse({"success": True,}, status = 200)

    return JsonResponse({"success": False}, status=400)