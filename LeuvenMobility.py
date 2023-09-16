import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.title("Leuven Multi-Modal Mobility hubs")
st.image('data/mobility_hubs_viz.webp')
st.sidebar.success("Open Solution or User page above.")

st.write("Hello!👋 This is the web interface of the proposed solution for the Leuven city challenge of the hackathon provided by MobilityDataLab.")
st.markdown(
    """
    Leuven Challenge
    - Check out our 2-stage solution with "Solution page"
    - Developed by OREH team (Slava Gorchakov)
"""
)