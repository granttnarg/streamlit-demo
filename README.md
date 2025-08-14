# 🌎 Global Development Data Visualization Dashboard

An interactive Streamlit web application for exploring relationships between economic indicators, poverty rates, and life expectancy across countries and time periods.

[Deployed Interactive App can be found here.](https://granttnarg-streamlit-demo-practical-g2lbi4.streamlit.app/)

## Overview

This demo project demonstrates **data visualization and interactive dashboard development** using Streamlit and Plotly. The focus is on creating intuitive, responsive visualizations that allow users to explore global country data and understand disparities in world economic factor over time using real data.

**Note**: This was primarily an exercise in visualization and UI development with Streamlit - the ML model serves as a simple interactive prediction feature rather than a sophisticated analytical tool.

## Features

- **Interactive Scatter Plots**: Dynamic visualizations with bubble sizing based on poverty rates
- **Multi-Tab Interface**: Global overview, country deep dive, and data explorer views
- **Real-time Filtering**: Year sliders and country selection with instant chart updates
- **ML Prediction Tool**: Simple Random Forest model for life expectancy prediction
- **Custom Styling**: Responsive layouts with custom CSS and audio feedback

## Tech Stack

- **Frontend**: Streamlit
- **Visualization**: Plotly Express
- **Data Processing**: Pandas
- **ML**: Scikit-learn (Random Forest)
- **Image Processing**: Pillow
- **Audio**: Base64 encoding for sound effects

## Installation

```bash
git clone granttnarg/streamlit-demo
cd streamlit-demo
pip install -r requirements.txt
streamlit run practical.py
```

## Usage

Run the app locally and navigate through three main tabs:

1. **Global Overview** - Explore year-by-year trends and test ML predictions
2. **Country Deep Dive** - Detailed metrics for individual countries
3. **Data Explorer** - Browse and filter the raw dataset

## Dataset

Global development indicators including:

- GDP per capita by country and year
- Life expectancy data (IHME estimates)
- Poverty rates across multiple poverty lines
- Income inequality measures (Gini coefficient, Palma ratio)
- Wealth distribution metrics (top 10% share)

## Project Structure

```
├── practical.py              # Main app entry point
├── model.py                   # ML model utilities
├── tab1_global_overview.py    # Global trends visualization
├── tab2_country_deep_dive.py  # Country-specific analysis
├── tab3_data_explorer.py      # Data browsing interface
├── requirements.txt           # Dependencies
└── global_development_data.csv # Dataset
```

## Key Learning Outcomes

- **Streamlit Development**: Multi-tab layouts, session state, interactive widgets
- **Data Visualization**: Effective use of Plotly for responsive charts
- **UI/UX Design**: Custom styling, layout optimization, user feedback
- **Data Pipeline**: Model persistence, data filtering, error handling

## Future Enhancements

While this project focused on visualization, potential extensions include:

- Adding complexity to the model and predictions
- Refactoring and refinding of the code base structure
- Advanced statistical analysis

---
