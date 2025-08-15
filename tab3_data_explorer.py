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
    
    # Add centered title above the layout
    st.markdown('<div style="text-align: center;"><h3>Data Explorer</h3></div>', unsafe_allow_html=True)
    
    # Create layout with narrow controls on left and map on right
    left_col, right_col = st.columns([1, 4])
    
    with left_col:
        st.markdown('<div style="margin-top: 100px;"></div>', unsafe_allow_html=True)
        year_range = st.slider(
          'Select Year',
          min_value=min_year,
          max_value=max_year,
          value=(min_year, max_year)
        )

        selected_countries = st.multiselect(
                                            'Select Countries',
                                            options=countries,
                                            default=countries[:5],
                                            key="data_explorer_countries"
        )

    with right_col:
        if selected_countries:
            # Calculate average GDP across the selected year range
            gdp_data = df[
                (df['country'].isin(selected_countries)) &
                (df['year'] >= year_range[0]) &
                (df['year'] <= year_range[1])
            ].groupby('country')['GDP per capita'].mean().reset_index()

            # Rename for clarity
            gdp_data.rename(columns={'GDP per capita': 'Avg GDP per capita'}, inplace=True)

            # Merge with coordinates
            map_data = coords_df[coords_df['country'].isin(selected_countries)].merge(
                gdp_data,
                on='country',
                how='left'
            )

            # Clean the data - this is the crucial step!
            map_data['Avg GDP per capita'] = map_data['Avg GDP per capita'].fillna(0)

            # Optional: Also remove any remaining NaN values just to be safe
            map_data = map_data.dropna(subset=['lat', 'long', 'Avg GDP per capita'])

            if not map_data.empty:
                fig_map = px.scatter_geo(
                    map_data,
                    lat='lat',
                    lon='long',
                    size='Avg GDP per capita',
                    hover_name='country',
                    hover_data={'Avg GDP per capita': ':$,.0f'},
                    title=f"Selected Countries - Average GDP per Capita ({year_range[0]}-{year_range[1]})",
                    projection="equirectangular",
                    size_max=8,
                    color='country'  # This assigns different colors per country
                )

                # Customize the map - REMOVE the color override
                fig_map.update_traces(
                    marker=dict(
                        line=dict(width=2, color='darkblue'),  # Fixed border color
                        sizemode='diameter'
                    )
                )
                # Don't override the color here - let Plotly use the automatic colors

                fig_map.update_layout(
                    height=600,
                    title_x=0.2,  # Center the title
                    geo=dict(
                        showframe=False,
                        showcoastlines=True,
                        coastlinecolor='rgb(204, 204, 204)',
                        projection_type='natural earth',  # Better projection
                        bgcolor='rgb(243, 243, 243)',
                        showland=True,
                        landcolor='rgb(243, 243, 243)',
                        showocean=True,
                        oceancolor='rgb(204, 230, 255)',
                        showlakes=True,
                        lakecolor='rgb(153, 204, 255)',
                        showcountries=True,
                        countrycolor='rgb(204, 204, 204)',
                        countrywidth=0.5,
                        resolution=50  # Higher resolution
                    )
                )

                st.plotly_chart(fig_map, use_container_width=True)
            else:
                st.write("No GDP data available for selected countries and years")
        else:
            st.write("Select countries to see them on the map")

    # Filter data based on selections
    filtered_df = df[
          (df['year'] >= year_range[0]) &
          (df['year'] <= year_range[1]) &
          (df['country'].isin(selected_countries))
      ]

    if not filtered_df.empty and len(selected_countries) >= 1:
        # Create comparison for selected countries
        comparison_data = filtered_df.groupby('country').agg({
            'GDP per capita': 'mean',
            'Life Expectancy (IHME)': 'mean',
            'gini': 'mean',
            'headcount_ratio_international_povline': 'mean'
        }).reset_index()

        # Normalize data for comparison (0-100 scale)
        for col in ['GDP per capita', 'Life Expectancy (IHME)']:
            comparison_data[f'{col}_norm'] = (comparison_data[col] / comparison_data[col].max()) * 100

        # Invert poverty and inequality (lower is better)
        for col in ['gini', 'headcount_ratio_international_povline']:
            comparison_data[f'{col}_norm'] = (1 - comparison_data[col] / comparison_data[col].max()) * 100

        fig_radar = px.bar(
            comparison_data,
            x='country',
            y=['GDP per capita_norm', 'Life Expectancy (IHME)_norm', 'gini_norm', 'headcount_ratio_international_povline_norm'],
            title="Normalized Country Performance (100 = Best)",
            barmode='group',
            height=100
        )
        fig_radar.update_layout(height=300, xaxis_tickangle=-45)
        st.plotly_chart(fig_radar, use_container_width=True)

    st.write(f'### World Data {year_range[0]} - {year_range[1]}')
    st.dataframe(data=filtered_df, selection_mode="multi-row")
    
    # Convert filtered dataframe to CSV for download
    csv_data = filtered_df.to_csv(index=False)
    st.download_button(
        label="Download Filtered Data",
        data=csv_data,
        file_name="filtered_data.csv",
        mime="text/csv"
    )