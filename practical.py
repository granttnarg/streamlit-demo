import streamlit as st
import pandas as pd
import base64
import numpy as np
from model import create_model
from PIL import Image

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

model, score = create_model('global_development_data.csv')

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
  st.scatter_chart(data=filtered_df, x="GDP per capita", y="Life Expectancy (IHME)",
                  x_label="GDP per Capita", height=250, y_label="Life Expectancy",
                  color="#008000", use_container_width=True)

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
      st.write(f"Predicted Life Expectancy: **{prediction:.1f} years**")
  with b:
    st.metric("Model R² Score", f"{score:.3f}")

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
                </style>
              """,
    unsafe_allow_html=True,
  )

with tab2:
   st.write("Work in Progress, Come back soon Ya'll! ")
with tab3:
  year_range = st.slider(
    'Select Year',
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
  )

  selected_countries = st.multiselect(
                                      'Select Countries',
                                      options=countries,
                                      default=countries[5],
                                      key="data_explorer_countries"
  )

  filtered_df = df[
        (df['year'] >= year_range[0]) &
        (df['year'] <= year_range[1]) &
        (df['country'].isin(selected_countries))
    ]

  st.dataframe(data=filtered_df, selection_mode="multi-row")
  st.markdown(download_csv('Filtered Data Frame',filtered_df),unsafe_allow_html=True)



#task 6 in tab 1: create a simple model (conda install scikit-learn -y; Randomforest Regressor): features only 3 columns: ['GDP per capita', 'headcount_ratio_upper_mid_income_povline', 'year']; target: 'Life Expectancy (IHME)'
#you might store the code in an extra model.py file
#make input fields for inference of the features (according to existing values in the dataset) and use the model to predict the life expectancy for the input values
#additional: show the feature importance as a bar plot