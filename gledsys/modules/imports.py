import csv
from uploads.models import Lightning
from django.utils.timezone import make_aware
from django.utils.dateparse import parse_datetime
from django.contrib.gis.geos import Point

def handle_lighting_data(obj):
    # Load CSV from storage
    tmp_data = []
    with open(obj.files.path, 'r') as f:
        data = csv.reader(f)
        next(data)
        for i, row in enumerate(data):
            parsed_datetime = make_aware(parse_datetime(row[2]))
            lighting = Lightning(
                datetime_utc = parsed_datetime,
                latitude = row[3],
                longitude = row[4],
                type = row[5],
                files_id = obj.id,
                coord = Point((float(row[4]), float(row[3])))
            )
            tmp_data.append(lighting)
    Lightning.objects.bulk_create(tmp_data)
