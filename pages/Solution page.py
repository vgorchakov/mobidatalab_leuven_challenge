import streamlit as st
import pandas as pd
import io
from PIL import Image
import base64
import plotly.graph_objects as go
import os
from pyproj import Transformer

MAPBOX_TOKEN = "pk.eyJ1IjoiZ29yY2hha292diIsImEiOiJjbDh4NmU4d3AwM3ljM3dsaDcyYnd4NzdsIn0.whPFq3l9sGBowsYjqS9WjQ" #os.getenv("MAPBOX_TOKEN")

st.title("Mobility hubs in Leuven")

mobility_hubs = pd.read_csv('data/mobility_hubs.csv')
mobility_hubs['lat'] = mobility_hubs['Y.1']
mobility_hubs['lon'] = mobility_hubs['X.1']
mobility_hubs['name'] = mobility_hubs['naam punt']


st.header("Solution Structure")
st.markdown("""
            We are investigating the opportunity of finding optimal locations for multi-modal mobility hubs on top of the existing hubs. 
            The cost of moving an existing hub can be quite high, so we are working in the assumption 
            that we want to ingest no more than X new locations in addition to existing ones in an optimal way.
            Let's first look on the existing mobility hubs on the map:
            """)
def build_markers_map(mobility_hubs,
                    MAPBOX_TOKEN):
    fig = go.Figure()
    fig.add_trace(
        go.Scattermapbox(
            mode="markers+text",
            lat=mobility_hubs['lat'].tolist(),
            lon=mobility_hubs['lon'].tolist(),
            marker={"size": 10, "color": "blue"},
            hovertext=mobility_hubs['name'],
        )
    )

    fig.update_layout(mapbox={
        "accesstoken": MAPBOX_TOKEN,
        "zoom": 12,
        "center": {
            "lat": pd.concat([mobility_hubs['lat'], mobility_hubs['lat']], axis=0).mean(),
            "lon": pd.concat([mobility_hubs['lon'], mobility_hubs['lon']], axis=0).mean(),
        },
    },
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
    )
    return fig
st.subheader("Current multi-modal mobility hub locations")
st.plotly_chart(build_markers_map(mobility_hubs, MAPBOX_TOKEN))

st.markdown("""
            The proposed solution consists of 3 principal layers: 
            - Multi-Criteria Analysis (MCA) with the Analytic Hierarchy Process (AHP) 
            - Multi-objective optimization model
            - App design and intergration to other services
            
            Let's investigate each stage step-by-step
            """)

st.subheader("Multi-Criteria Analysis (MCA) with the Analytic Hierarchy Process (AHP)")
st.markdown("""
            The process of multi-criteria analysis consist of several steps. We are going to provide a design of this 
            analysis based on demographic data of Leuven city included as an input of the challenge
            - Identifying Criteria: The first step is to identify and define the relevant criteria that will be used 
            to evaluate alternatives. Based on input demographic data we can identify the following criteria for neighbourhood: 
            overall population, percentage of middle-aged adults who identify as a car user, percentage of students,
            median income, percentage of householdes with at least one bike available, 
            percentage of population not holding a driver license, etc. 
            - Weighting Criteria: evaluated with Analytic Hierarchy Process (AHP). We use a Pairwise Comparison Matrix: 
            For each pair of criteria and alternatives, a matrix is created in which you compare their relative importance and evaluate scores.
            - Identifying Alternatives: List the neighborhoods or locations you are considering for the mobility hub placement.
            - Evaluating assessment of Alternatives: Based on the calculated weighted sums, rank the neighborhoods in descending order. 
            The neighborhood with the highest weighted sum will be ranked the highest and considered the most suitable 
            for placing the mobility hub.
            As an output from this stage we are going to take indicator (score) of Neighbourhood attractiveness 
            in the context of mobility hub placement.
            """)
st.subheader("Multi-objective optimization model")
st.markdown("""
            To use the full power of discrete optimization methods we are going to transform our data to node-based approach.
            For each neighbourhood we compute the centroid and link data associated with this neighbourhood 
            (demographic data, demand and supply data, etc.) with the computed centroid.
            """)
st.image("data/centroids.png")
st.markdown("""
            To formulate an efficient optimization model we need to defined 2 main components: constraints
            and objectives.
            """)
st.divider()
st.markdown("""
            Objective: free and commercial solvers allows to solve the optimization model with multiple objectives.
            In our case the first objective will be minimization of total duration time of all potential mobility hubs 
            users. We will use a weighted sum and multiplicator to this duration time will be defined as 
            [Neighbourhood Car Demand * Neighbourhood Attractiveness Indicator] where "Neighbourhood Car Demand" is taken
            from demand/supply data and Neighbourhood Attractiveness Indicator is computed in 1st stage of solution.
            
            So, Obj. 1: MIN(Total duration time * [Neighbourhood Car Demand * Neighbourhood Attractiveness Indicator]) 
            
            Second objective can be defined as minimization of operational opening cost of new hubs.
            This factor depends on how expensive is to build a new hub in specific area.
            
            Obj. 2: MIN(Operational New Hubs Opening Cost) 
            
            Optimization modelling allows to consider different ways of objective prioritization. We can take a weighed 
            sum of these two objectives or indicate the prioritization explicitly (first optimize Obj.1, then Obj.2)
            """)
st.divider()
st.markdown("""
            Constraints: the real power of optimization model solution is an opportunity to add new business constraints
            after the first iterations of solving. 
            Let's list the most obvious constraints that will arise during the process of industrialization of our solution:
            - number of new hubs < X
            - distance(hub, closest off-street parking) < Y
            - sum of hubs group capacity >= demand of local neighbourhoods 
            - X, Y - configurable parameters
            """)
st.divider()
st.markdown("""
            The output of an optimization model - locations of extra multi-modal mobility hubs.""")
# Display teams map
st.subheader("Optimized multi-modal mobility hub locations")



mobility_hubs_suggestions = pd.read_csv('data/mobility_hubs_suggestions.csv')
def build_markers_map(mobility_hubs, mobility_hubs_suggestions,
                    MAPBOX_TOKEN):
    fig = go.Figure()
    fig.add_trace(
        go.Scattermapbox(
            mode="markers+text",
            lat=mobility_hubs['lat'].tolist(),
            lon=mobility_hubs['lon'].tolist(),
            marker={"size": 10, "color": "blue"},
            hovertext=mobility_hubs['name'],
        )
    )

    fig.add_trace(
        go.Scattermapbox(
            mode="markers+text",
            lat=mobility_hubs_suggestions['lat'].tolist(),
            lon=mobility_hubs_suggestions['lon'].tolist(),
            marker={"size": 12, "color": "green"},
            hovertext=mobility_hubs_suggestions['name'],
        )
    )

    fig.update_layout(mapbox={
        "accesstoken": MAPBOX_TOKEN,
        "zoom": 12,
        "center": {
            "lat": pd.concat([mobility_hubs['lat'], mobility_hubs['lat']], axis=0).mean(),
            "lon": pd.concat([mobility_hubs['lon'], mobility_hubs['lon']], axis=0).mean(),
        },
    },
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=True,
    )
    return fig

st.plotly_chart(build_markers_map(mobility_hubs, mobility_hubs_suggestions, MAPBOX_TOKEN))

transformer = Transformer.from_crs("EPSG:31370", "EPSG:4326")
centroids_sector = pd.read_csv('data/centroids_areas.csv')
centroids_sector['lat'], centroids_sector['lon'] = transformer.transform(centroids_sector['X'], centroids_sector['Y'])
centroids_sector['name'] = centroids_sector['CODSEC']
