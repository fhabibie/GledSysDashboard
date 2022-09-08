import csv
from uploads.models import Lightning
def handle_lighting_data(obj):
    # Load CSV from storage
    tmp_data = []
    with open(obj.files.path, 'r') as f:
        data = csv.reader(f)
        next(data)
        for i, row in enumerate(data):
            print('saving', i)
            lighting = Lightning(
                datetime_utc = row[2],
                latitude = row[3],
                longitude = row[4],
                type = row[5],
                files_id = obj.id,
            )
            tmp_data.append(lighting)
    Lightning.objects.bulk_create(tmp_data)
