import streamlit as st
import pandas as pd
import base64
import numpy as np
import sys
import os
from model import get_or_create_model
from PIL import Image
import plotly.express as px

sys.path.append(os.path.dirname(__file__))

import base64

def get_audio_base64(audio_file_path):
    with open(audio_file_path, "rb") as audio_file:
        audio_bytes = audio_file.read()
    audio_base64 = base64.b64encode(audio_bytes).decode()
    return audio_base64

def play_impact_sound():
    audio_base64 = get_audio_base64("impact.mp3")  # Your sound file
    audio_html = f"""
    <audio autoplay>
        <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
    </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

# Load and crop image
image = Image.open("life_2.jpg")

header_image = image.crop((0, 200, image.width, 1200))  # Shows top 200 pixels

st.write("# 🌎 Worldwide Analysis of Quality of Life and Economic Factors")
st.write("This app enables you to explore the relationships between poverty, life expectancy, and GDP across various countries and years. Use the panels to select options and interact with the data.")
st.image(header_image, use_container_width=True)

tabs = ["Global Overview", "Country Deep Dive", "Data Explorer"]
tab1, tab2, tab3 = st.tabs(tabs, width="stretch")

df = pd.read_csv("./global_development_data.csv")

min_year = int(df['year'].min())
max_year = int(df['year'].max())
countries = sorted(df['country'].unique())

def download_csv(name,df):

  csv = df.to_csv(index=False)
  base = base64.b64encode(csv.encode()).decode()
  file = (f'<a href="data:file/csv;base64,{base}" download="%s.csv">Download file</a>' % (name))

  return file

model, score = get_or_create_model('global_development_data.csv')

with tab1:
  year = st.slider(
      'Select Year',
      min_value=min_year,
      max_value=max_year,
      value=(max_year)
  )

  # THEN filter and plot
  filtered_df = df[(df['year'] == year)]
  st.write("### GDPPC over Life Expectancy")
  fig = px.scatter(filtered_df, x="GDP per capita", y="Life Expectancy (IHME)",
                  labels={"GDP per capita": "GDP per Capita",
                        "Life Expectancy (IHME)": "Life Expectancy"},
                  color="country")

  st.write(f'#### ML Predictor for {year}')
  gdp = st.slider(
      "GDP per capita",
      min_value=int(df['GDP per capita'].min()),
      max_value=int(df['GDP per capita'].max()),
      value=int(df['GDP per capita'].mean())  # or median()
  )

  poverty = st.slider(
      "Poverty ratio",
      min_value=float(df['headcount_ratio_upper_mid_income_povline'].min()),
      max_value=float(df['headcount_ratio_upper_mid_income_povline'].max()),
      value=float(df['headcount_ratio_upper_mid_income_povline'].mean())
  )
  filtered_df = df[(df['year'] == year)]

  a, b = st.columns(2)

  with a:
    if st.button("Predict"):
        prediction = model.predict([[gdp, poverty, year]])[0]
        st.session_state.prediction = prediction
        st.write(f"Predicted Life Expectancy: **{prediction:.1f} years**")
        play_impact_sound()
  with b:
    st.metric("Model R² Score", f"{score:.3f}")

  # Add prediction point if it exists
  if st.session_state.get('prediction'):
      prediction_value = st.session_state.prediction
      fig.add_scatter(x=[gdp], y=[prediction_value],
                    mode='markers+text',
                    marker=dict(symbol='circle', size=20, color='red', opacity=0),
                    text='💀',
                    textfont=dict(size=20),
                    name='Prediction')

  # Display chart only once, outside columns
  fig.update_layout(height=350)
  st.plotly_chart(fig, use_container_width=True)

  mean_life_expectancy = filtered_df['Life Expectancy (IHME)'].mean()
  mean_gdp_per_capita = filtered_df['GDP per capita'].mean()
  number_of_countries = len(filtered_df['country'].unique())
  mean_headcount_ratio_upper_mid_income_povline = filtered_df['headcount_ratio_upper_mid_income_povline'].mean()

  st.write(f'#### Data for {year}')
  st.dataframe(data=filtered_df, selection_mode="multi-row")

  with st.sidebar:
      st.header("📊 Dataset Overview")
      st.metric("Total Countries", len(countries))
      st.metric("Year Range", f"{min_year} - {max_year}")
      st.metric("Total Records", len(df))
      st.metric("Model Accuracy (R²)", f"{score:.3f}")

      st.header(f'📊 {year} Metrics')
      col1, col2 = st.columns(2)
      st.metric("Mean Life Expectancy", f"{mean_life_expectancy:.2f} years")
      st.metric("Mean GDP per capita", f"{mean_gdp_per_capita:.2f}")
      st.metric("Country Count", f"{number_of_countries}")
      st.metric("Mean Ratio Poverty Line", f"{mean_headcount_ratio_upper_mid_income_povline:.2f}")

  st.markdown(
             """
                <style>
                [data-testid="stMetricValue"] {
                    font-size: 18px;
                }
                .main .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                    padding-left: 1rem;
                    padding-right: 1rem;
                    max-width: 100%;
                }

                .stTabs [data-baseweb="tab-list"] {
                    margin-left: 0;
                    margin-right: 0;
                }

                .element-container {
                    margin: 0 !important;
                    padding: 0 !important;
                }
                </style>
              """,
    unsafe_allow_html=True,
  )

with tab2:


  country = st.selectbox(
                                    'Select Countries',
                                    options=countries,
                                    index=0,
                                    key="data_explorer_country"
  )

  filtered_df = df[
        (df['country'] == country)
    ]

  if not filtered_df.empty:
    # Calculate smart aggregations
    latest_year = filtered_df['year'].max()
    earliest_year = filtered_df['year'].min()

    st.write(f"### 📊 {country} Overview ({earliest_year}-{latest_year})")

    t2a, t2b, t2c = st.columns(3)

    with t2a:
      # Economic Indicators - use latest for current state
      latest_gdp = filtered_df[filtered_df['year'] == latest_year]['GDP per capita'].iloc[0]
      avg_gini = filtered_df['gini'].mean()

      st.metric(
        "💰 GDP per Capita (Latest)",
        f"${latest_gdp:,.0f}",
        help=f"Most recent GDP per capita ({latest_year})"
      )
      st.metric(
        "📊 Avg Gini Coefficient",
        f"{avg_gini:.3f}",
        help="Average income inequality over time"
      )

    with t2b:
      # Health - latest is best for current state
      latest_life = filtered_df[filtered_df['year'] == latest_year]['Life Expectancy (IHME)'].iloc[0]
      avg_poverty = filtered_df['headcount_ratio_international_povline'].mean()

      st.metric(
        "❤️ Life Expectancy (Latest)",
        f"{latest_life:.1f} years",
        help=f"Current life expectancy ({latest_year})"
      )
      st.metric(
        "🌍 Avg International Poverty",
        f"{avg_poverty:.1f}%",
        help="Average poverty rate over time"
      )

    with t2c:
      # Wealth Distribution - averages work well
      avg_top10 = filtered_df['decile10_share'].mean()
      avg_palma = filtered_df['palma_ratio'].mean()

      st.metric(
        "🔝 Avg Top 10% Share",
        f"{avg_top10:.1f}%",
        help="Average wealth concentration over time"
      )
      st.metric(
        "⚖️ Avg Palma Ratio",
        f"{avg_palma:.2f}",
        help="Average inequality measure over time"
      )

  st.dataframe(data=filtered_df, selection_mode="multi-row")
with tab3:
  # Load the coordinates CSV
  coords_df = pd.read_csv("countries_coordinates.csv")

  year_range = st.slider(
    'Select Year',
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
  )

  selected_countries = st.multiselect(
                                      'Select Countries',
                                      options=countries,
                                      default=[countries[5]],  # Changed to list
                                      key="data_explorer_countries"
  )

  st.write("### Interactive World Map")
  # Merge coordinates with your data for selected countries
  map_data = coords_df[coords_df['country'].isin(selected_countries)].copy()
  if not map_data.empty:
    # Create the world map
    fig_map = px.scatter_geo(
        map_data,
        lat='lat',
        lon='long',
        hover_name='country',
        title="Selected Countries",
        projection="equirectangular",
    )
    # Customize the map
    fig_map.update_traces(
        marker=dict(
            size=12,
            color='red',
            symbol='circle',
            line=dict(width=2, color='darkred')
        )
    )

    fig_map.update_layout(
        width=500,
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='equirectangular'
        )
    )
    st.plotly_chart(fig_map, use_container_width=True)
  else:
    st.write("Select countries to see them on the map")

  # Filter data based on selections
  filtered_df = df[
        (df['year'] >= year_range[0]) &
        (df['year'] <= year_range[1]) &
        (df['country'].isin(selected_countries))
    ]

  st.write(f'### World Data {year_range[0]} - {year_range[1]}')
  st.dataframe(data=filtered_df, selection_mode="multi-row")
  st.markdown(download_csv('Filtered Data Frame',filtered_df),unsafe_allow_html=True)