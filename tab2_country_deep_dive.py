import streamlit as st
import pandas as pd


def render_tab2(df, countries):
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