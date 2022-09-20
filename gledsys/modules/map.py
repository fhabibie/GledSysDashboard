from uploads.models import Lightning
import geopandas as gpd
import pandas as pd
import pygmt
import base64

def get_distribution_map(obj=[], boundary=(94, -12, 144, 10)):
    # Boundary (min_long, min_lat, max_long, max_lat)
    if len(obj) <= 0:
        # Return basemap
        region = [boundary[0], boundary[2], boundary[1], boundary[3]]
        fig = pygmt.Figure()
        fig.basemap(region=region, projection="M15c", frame=True)
        fig.coast(land="black", water="skyblue")

        raw_png = fig._preview(fmt="png", dpi=300, anti_alias=True, as_bytes=True)
        base64_png = base64.encodebytes(raw_png)
        res = base64_png.decode("utf-8")

        return res
    else:
        df = pd.DataFrame(list(obj), columns=["datetime_utc", "latitude", "longitude", "type"])
        # df['color'] = df['type'].apply(lambda x: 'magenta4' if x == 2 else 'seagreen' if x == 1 else 'darkorange')

        print(df)
        
        df_gcp = df[df.type == 0]
        df_gcn = df[df.type == 1]
        df_ic = df[df.type == 2]

        region = [boundary[0] - 2, boundary[2] + 2, boundary[1] - 2, boundary[3] + 2]

        fig = pygmt.Figure()
        fig.basemap(region=region, projection="M15c", frame=True)
        fig.coast(land="black", water="skyblue")
        
        if len(df_ic) > 0:
            fig.plot(x=df_ic.longitude, y=df_ic.latitude, style="c0.3c", color="magenta4", pen="black")
        if len(df_gcn) > 0:
            fig.plot(x=df_gcn.longitude, y=df_gcn.latitude, style="c0.3c", color="green", pen="black")
        if len(df_gcp) > 0:
            fig.plot(x=df_gcp.longitude, y=df_gcp.latitude, style="c0.3c", color="darkorange", pen="black")

        raw_png = fig._preview(fmt="png", dpi=300, anti_alias=True, as_bytes=True)
        base64_png = base64.encodebytes(raw_png)
        res = base64_png.decode("utf-8")

        return res
