from uploads.models import Lightning
import geopandas as gpd
import pandas as pd
import pygmt
import base64

def get_distribution_map(obj, boundary):
    # Boundary (min_long, min_lat, max_long, max_lat)
    # df = gpd.GeoDataFrame(list(obj), columns=["datetime_utc", "coord", "type"])
    df = pd.DataFrame(list(obj), columns=["datetime_utc", "latitude", "longitude", "type"])
    df_gcp = df[df.type == 0]
    df_gcn = df[df.type == 1]
    df_ic = df[df.type == 2]

    region = [
        boundary[0] - 2,
        boundary[2] + 2,
        boundary[1] - 2,
        boundary[3] + 2,
    ]

    # region = [ 94, 144, -12, 10] # Indonesia reg

    print(region)
    fig = pygmt.Figure()
    fig.basemap(region=region, projection="M15c", frame=True)
    fig.coast(land="black", water="skyblue")
    fig.plot(x=df_ic.longitude, y=df_ic.latitude, style="c0.2c", color="magenta4", pen="black")
    fig.plot(x=df_gcp.longitude, y=df_gcp.latitude, style="khurricane/0.3c", color="seagreen", pen="black")
    fig.plot(x=df_gcn.longitude, y=df_gcn.latitude, style="kflash/0.3c", color="darkorange", pen="black")

    raw_png = fig._preview(fmt="png", dpi=300, anti_alias=True, as_bytes=True)
    base64_png = base64.encodebytes(raw_png)
    res = base64_png.decode("utf-8")

    return res