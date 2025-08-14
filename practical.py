import streamlit as st
import pandas as pd
import sys
import os
from model import get_or_create_model
from PIL import Image
from tab1_global_overview import render_tab1
from tab2_country_deep_dive import render_tab2
from tab3_data_explorer import render_tab3

sys.path.append(os.path.dirname(__file__))

# Load and crop image
image = Image.open("life_2.jpg")

header_image = image.crop((0, 200, image.width, 1200))

st.write("# 🌎 Worldwide Analysis of Quality of Life and Economic Factors")
st.write("This app enables you to explore the relationships between poverty, life expectancy, and GDP across various countries and years. Use the panels to select options and interact with the data.")
st.image(header_image, use_container_width=True)

tabs = ["Global Overview", "Country Deep Dive", "Data Explorer"]
tab1, tab2, tab3 = st.tabs(tabs, width="stretch")

df = pd.read_csv("./global_development_data.csv")

min_year = int(df['year'].min())
max_year = int(df['year'].max())
countries = sorted(df['country'].unique())


model, score = get_or_create_model('global_development_data.csv')

with tab1:
    render_tab1(df, model, score, min_year, max_year, countries)
with tab2:
    render_tab2(df, countries)
with tab3:
    render_tab3(df, min_year, max_year, countries)