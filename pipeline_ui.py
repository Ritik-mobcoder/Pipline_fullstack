import streamlit as st
import requests
from PIL import Image
import io
import json

# Set the title for the app
st.title("Seaborn Dataset Visualization")

# Dropdown for selecting the dataset
dataset_name = st.selectbox(
    "Select a Seaborn Dataset:",
    ["tips"]
)

# FastAPI URL for before and after pipeline images
before_url = "http://127.0.0.1:8000/before-pipeline"
after_url = "http://127.0.0.1:8000/after-pipeline"

# Button to fetch and display results
if st.button("Show Before and After Pipeline Plots"):
    # Prepare the payload to send to the FastAPI server
    payload = {"dataset_name": dataset_name}

    # Fetch the "before-pipeline" plot
    st.subheader("Before Pipeline Transformation")
    before_response = requests.get(before_url, json=payload)  # Use get request
    if before_response.status_code == 200:
        # Display the image from the before-pipeline API
        before_image = Image.open(io.BytesIO(before_response.content))
        st.image(before_image, caption="Before Pipeline Plot", use_column_width=True)
    else:
        st.error(f"Error fetching data from {before_url}")

    # Fetch the "after-pipeline" plot
    st.subheader("After Pipeline Transformation")
    after_response = requests.get(after_url, json=payload)  # Use get request
    if after_response.status_code == 200:
        # Display the image from the after-pipeline API
        after_image = Image.open(io.BytesIO(after_response.content))
        st.image(after_image, caption="After Pipeline Plot", use_column_width=True)
    else:
        st.error(f"Error fetching data from {after_url}")
