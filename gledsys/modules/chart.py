import base64
from io import BytesIO
import matplotlib.pyplot as plt
import plotly.express as px
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

def get_lightning_bar_chart(obj):
    plt.switch_backend('AGG')
    df = pd.DataFrame(list(obj), columns=["datetime_utc", "type"])
    df['datetime_utc'] = df['datetime_utc'].dt.strftime('%m/%d/%Y')
    df['category'] = df['type'].apply(lambda x: 'IC' if x == 2 else 'GC-' if x == 1 else 'GC+')
    df = df.groupby(['datetime_utc', 'category']).size().unstack()
    df.plot(kind='bar', stacked=True, figsize=(8,5), rot=90, title="Lightning Statistics", xlabel="Date")
    
    plt.subplots_adjust(bottom=0.3)
    chart = get_base64()
    return chart

def get_lightning_pie_chart(obj):
    plt.switch_backend('AGG')
    df = pd.DataFrame(list(obj), columns=["datetime_utc", "type"])
    df['category'] = df['type'].apply(lambda x: 'IC' if x == 2 else 'GC-' if x == 1 else 'GC+')
    df = df.groupby(['category']).size()
    df.plot(kind='pie', y='category', figsize=(8,5), autopct='%1.0f%%', title="Pie Lightning Statistics")

    chart = get_base64()
    return chart

def get_lightning_pie_chart_plotly(obj):
    df = pd.DataFrame(list(obj), columns=["datetime_utc", "type"])
    df['category'] = df['type'].apply(lambda x: 'IC' if x == 2 else 'GC-' if x == 1 else 'GC+')
    df = df.groupby(['category'], as_index=False, group_keys=True).size()
    fig = px.pie(df, values='size', names='category')

    return fig.to_html()

def get_lightning_bar_chart_plotly(obj):
    df = pd.DataFrame(list(obj), columns=["datetime_utc", "type"])
    df['datetime_utc'] = df['datetime_utc'].dt.strftime('%m/%d/%Y')
    df['category'] = df['type'].apply(lambda x: 'IC' if x == 2 else 'GC-' if x == 1 else 'GC+')
    df = df.groupby(['datetime_utc', 'category'], as_index=False).size()
    fig = px.bar(df,x="datetime_utc", y="size", color="category", title="Bar chart", 
        color_discrete_map={
            'GC+': '#ff7800',
            'GC-': '#94fc03',
            'IC': '#7703fc',
        })

    return fig.to_html()
