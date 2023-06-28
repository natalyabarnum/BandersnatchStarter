import altair as alt
from altair import Chart, Tooltip
from app.data import Database
import pandas as pd


db = Database()
df = db.dataframe()

def chart(df=df, x=str, y=str, target=str) -> Chart:
    graph = Chart(df, width=400, height=400, title=f"{x} by {y} for {target}").mark_point().encode(
            x=x,
            y=y,
            color=alt.Color(target, scale=alt.Scale(scheme='viridis')),
            tooltip=Tooltip(df.columns.to_list())
    ).configure(
        padding=60
    ).configure_view(
        fill='#21201E',
        stroke='#21201E',
        strokeWidth=400
    ).configure_title(
        font='Arial',
        color='#E3DDD5',
        fontSize=30,
        offset=20,
        frame='bounds'
    ).configure_axis(
        labelColor='#E3DDD5',
        titleColor='#E3DDD5',
        domainWidth=1,
        gridWidth=0.2,
        labelFontSize=10,
        titleFontSize=13,
        titlePadding=10
    ).configure_legend(
        titleColor='#E3DDD5',
        labelColor='#E3DDD5',
        offset=20
    )

    graph.save('chart.html')
    graph.to_json()
    return graph

