import base64
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Convert chart images to base64
def get_base64():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    img_png = buffer.getvalue()
    res = base64.b64encode(img_png)
    res = res.decode('utf-8')
    buffer.close()

    return res

def get_lighting_bar_chart(obj):
    plt.switch_backend('AGG')
    df = pd.DataFrame(list(obj), columns=["datetime_utc", "type"])
    df['datetime_utc'] = df['datetime_utc'].dt.strftime('%m/%d/%Y')
    df['category'] = df['type'].apply(lambda x: 'IC' if x == 2 else 'GC-' if x == 1 else 'GC+')
    df = df.groupby(['datetime_utc', 'category']).size().unstack()
    df.plot(kind='bar', stacked=True, figsize=(8,5), rot=90, title="Lightning Statistics", xlabel="Date")
    
    plt.subplots_adjust(bottom=0.3)
    chart = get_base64()
    return chart

def get_lighting_pie_chart(obj):
    plt.switch_backend('AGG')
    df = pd.DataFrame(list(obj), columns=["datetime_utc", "type"])
    df['datetime_utc'] = df['datetime_utc'].dt.strftime('%m/%d/%Y')
    df['category'] = df['type'].apply(lambda x: 'IC' if x == 2 else 'GC-' if x == 1 else 'GC+')
    df = df.groupby(['category']).size()
    df.plot(kind='pie', y='category', figsize=(8,5), autopct='%1.0f%%', title="Pie Lightning Statistics")

    chart = get_base64()
    return chart
