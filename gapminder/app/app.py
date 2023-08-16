import os
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Specify the file paths
population_file = os.path.join(current_dir, "population_total.csv")
life_expectancy_file = os.path.join(current_dir, "life_expectancy_years.csv")
gni_per_capita_file = os.path.join(current_dir, "ny_gnp_pcap_cn.csv")

st.title('Gapminder')
st.write("Unlocking Lifetimes: Visualizing Progress in Longevity and Poverty Eradication")

@st.cache
def load_data():
    # Load the CSV files
    population_df = pd.read_csv(population_file)
    life_expectancy_df = pd.read_csv(life_expectancy_file)
    gni_per_capita_df = pd.read_csv(gni_per_capita_file)

    # Forward fill missing values
    population_df.fillna(method="ffill", inplace=True)
    life_expectancy_df.fillna(method="ffill", inplace=True)
    gni_per_capita_df.fillna(method="ffill", inplace=True)

    # Transform data into tidy format
    population_df = population_df.melt(id_vars=["country"], var_name="year", value_name="population")
    life_expectancy_df = life_expectancy_df.melt(id_vars=["country"], var_name="year", value_name="life_expectancy")
    gni_per_capita_df = gni_per_capita_df.melt(id_vars=["country"], var_name="year", value_name="gni_per_capita")

    # Merge the three dataframes
    merged_df = population_df.merge(life_expectancy_df, on=["country", "year"])
    merged_df = merged_df.merge(gni_per_capita_df, on=["country", "year"])

    # Convert 'gni_per_capita' column to numeric
    merged_df['gni_per_capita'] = pd.to_numeric(merged_df['gni_per_capita'], errors='coerce')

    return merged_df

data = load_data()

# Convert 'population' and 'gni_per_capita' columns to numeric
data['population'] = pd.to_numeric(data['population'], errors='coerce')
data['gni_per_capita'] = pd.to_numeric(data['gni_per_capita'], errors='coerce')

# Replace NaN values in 'population' column with 0
data['population'].fillna(0, inplace=True)

# Replace NaN values in 'gni_per_capita' column with the mean value
mean_gni_per_capita = np.nanmean(data['gni_per_capita'])
data['gni_per_capita'].fillna(mean_gni_per_capita, inplace=True)

# Create the bubble chart using Plotly
fig = px.scatter(data_frame=data, x='gni_per_capita', y='life_expectancy', size='population',
                 color='country', log_x=True, hover_name='country', labels={'gni_per_capita': 'Gross National Income per Capita (log scale)'},
                 title='Gapminder: Unlocking Lifetimes')

# Display the chart
st.plotly_chart(fig)
