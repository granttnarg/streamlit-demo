import streamlit as st
import pandas as pd
import base64
import numpy as np

st.write("# Worldwide Analysis of Quality of Life and Economic Factors")
st.write("### This app enables you to explore the relationships between poverty, life expectancy, and GDP across various countries and years. Use the panels to select options and interact with the data.")

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

with tab1:
  year = st.slider(
    'Select Year',
    min_value=min_year,
    max_value=max_year,
    value=(max_year)
  )

  filtered_df = df[(df['year'] == year)]

  # filtered_df["GDP per capita Log"] = np.log10(df["GDP per capita"])
  st.write("### GDPPC over Life Expectancy")
  st.scatter_chart(data=filtered_df, x="GDP per capita", y="Life Expectancy (IHME)", x_label="GDP per Capita", height=200, y_label="Life Expectancy", color="#ffaa00", use_container_width=True)

  mean_life_expectancy = filtered_df['Life Expectancy (IHME)'].mean()
  mean_gdp_per_capita = filtered_df['GDP per capita'].mean()
  number_of_countries = len(filtered_df['country'].unique())
  mean_headcount_ratio_upper_mid_income_povline = filtered_df['headcount_ratio_upper_mid_income_povline'].mean()

  st.dataframe(data=filtered_df, selection_mode="multi-row")

  st.write("### Filtered Metrics")
  col1, col2 = st.columns(2)
  col3, col4 = st.columns(2)

  with col1:
      st.metric("Mean Life Expectancy", f"{mean_life_expectancy:.2f} years")
  with col2:
      st.metric("Mean GDP per capita", f"{mean_gdp_per_capita:.2f}")
  with col3:
      st.metric("Country Count", f"{number_of_countries}")
  with col4:
     st.metric("Mean HC Ratio Upper Mid Income Poverty Line", f"{mean_headcount_ratio_upper_mid_income_povline:.2f}")

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
