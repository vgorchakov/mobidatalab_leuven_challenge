import streamlit as st
import pandas as pd
import io
from PIL import Image
import base64
import plotly.graph_objects as go
import os

MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")

st.title("Mobility hubs in Leuven")

# @st.cache_resource
# def run_optimizer():
#     return run_pipeline()
#
# schedule = run_optimizer()


# Display teams map
st.header("Multi-modal mobility hub locations")

mobility_hubs = pd.read_csv('data/mobility_hubs.csv')
mobility_hubs['lat'] = mobility_hubs['Y.1']
mobility_hubs['lon'] = mobility_hubs['X.1']
mobility_hubs['name'] = mobility_hubs['naam punt']

def build_markers_map(df,
                    MAPBOX_TOKEN):
    fig = go.Figure()
    fig.add_trace(
        go.Scattermapbox(
            mode="markers+text",
            lat=df['lat'].tolist(),
            lon=df['lon'].tolist(),
            marker={"size": 10, "color": "black"},
            hovertext=df['name'],
        )
    )
    fig.update_layout(mapbox={
        "accesstoken": MAPBOX_TOKEN,
        "zoom": 12,
        "center": {
            "lat": pd.concat([df['lat'], df['lat']], axis=0).mean(),
            "lon": pd.concat([df['lon'], df['lon']], axis=0).mean(),
        },
    },
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
    )
    return fig

st.plotly_chart(build_markers_map(mobility_hubs, MAPBOX_TOKEN))


# Button to export schedule to XLSX

# download button 2 to download dataframe as xlsx
# buffer = io.BytesIO()
# with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
#     schedule.league_schedule_table.to_excel(writer, sheet_name='Schedule', index=False)
#
#     download2 = st.download_button(
#         label="Download schedule as Excel",
#         data=buffer,
#         file_name='bundesliga_schedule.xlsx',
#         mime='application/vnd.ms-excel'
#     )