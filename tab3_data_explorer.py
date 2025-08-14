import streamlit as st
import pandas as pd
import plotly.express as px
import base64


def download_csv(name, df):
    csv = df.to_csv(index=False)
    base = base64.b64encode(csv.encode()).decode()
    file = (f'<a href="data:file/csv;base64,{base}" download="%s.csv">Download file</a>' % (name))
    return file


def render_tab3(df, min_year, max_year, countries):
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