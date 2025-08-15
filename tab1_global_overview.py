import streamlit as st
import pandas as pd
import plotly.express as px
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


def render_tab1(df, model, score, min_year, max_year, countries):
    st.write("### GDP per Capita vs Life Expectancy")

    # Create main layout with sliders on left and plot on right
    left_col, right_col = st.columns([1, 2])

    with left_col:
        year = st.slider(
            'Select Year',
            min_value=min_year,
            max_value=max_year,
            value=(max_year)
        )

        st.write(f'#### ML Predictor for {year}')
        gdp = st.slider(
            "GDP per capita",
            min_value=int(df['GDP per capita'].min()),
            max_value=int(df['GDP per capita'].max()),
            value=int(df['GDP per capita'].mean())
        )

        poverty = st.slider(
            "Poverty ratio",
            min_value=float(df['headcount_ratio_upper_mid_income_povline'].min()),
            max_value=float(df['headcount_ratio_upper_mid_income_povline'].max()),
            value=float(df['headcount_ratio_upper_mid_income_povline'].mean())
        )

        if st.button("Predict"):
            prediction = model.predict([[gdp, poverty, year]])[0]
            st.session_state.prediction = prediction
            st.write(f"Predicted Life Expectancy: **{prediction:.1f} years**")
            play_impact_sound()

        st.metric("Model R² Score", f"{score:.3f}")

    with right_col:
        # Filter and plot
        filtered_df = df[(df['year'] == year)]
        fig = px.scatter(filtered_df, x="GDP per capita", y="Life Expectancy (IHME)",
                    labels={"GDP per capita": "GDP per Capita",
                          "Life Expectancy (IHME)": "Life Expectancy"},
                    color="country",
                    size="headcount_ratio_upper_mid_income_povline",
                    size_max=20,
                    hover_data={"headcount_ratio_upper_mid_income_povline": ":.1f%"})

        # Add prediction point if it exists
        if st.session_state.get('prediction'):
            prediction_value = st.session_state.prediction
            fig.add_scatter(x=[gdp], y=[prediction_value],
                          mode='markers+text',
                          marker=dict(symbol='circle', size=20, color='red', opacity=0),
                          text='💀',
                          textfont=dict(size=20),
                          name='Prediction')

        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    st.markdown(
    "<small style='font-size: 10px; color: gray;'>*scatter point size weighted on Poverty rate (Head count ratio upper mid income poverty line)</small>", 
    unsafe_allow_html=True
    )

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