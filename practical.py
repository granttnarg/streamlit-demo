import streamlit as st
import pandas as pd
import base64

st.write("# Worldwide Analysis of Quality of Life and Economic Factors")
st.write("#### This app enables you to explore the relationships between poverty, life expectancy, and GDP across various countries and years. Use the panels to select options and interact with the data.")

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

