import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

#Set Title Dashboard
st.title("IMDB Top 250 Movies Dashboard")

#Set header
st.header("Data Preview")
st.write("Berikut ini adalah dataset yang berisi 250 film dengan rating tertinggi menurut IMDB")

#Load data
path = "IMDB Top 250 Movies.csv"
imdb_data = pd.read_csv(path)
st.dataframe(imdb_data)

#Preprocess the dataset
def preprocess_column(column):
    return pd.to_numeric(imdb_data[column].str.replace(r"[\$,]", "", regex=True), errors="coerce")

imdb_data["budget"] = preprocess_column("budget")
imdb_data["box_office"] = preprocess_column("box_office")

#Treemap based on Genre
# Set Treemap based on Genre
st.header("Treemap: Movies by Genre")

# Preprocess genre data (splitting multiple genres into individual rows)
genre_data = imdb_data.copy()
genre_data = genre_data.assign(genre=genre_data['genre'].str.split(",")).explode('genre')

# Plot treemap
fig = px.treemap(
    genre_data,
    path=['genre', 'name'],
    values='rating',
    color='rating',
    color_continuous_scale='Blues',
    title="Treemap of Movies by Genre"
)
st.plotly_chart(fig)

#Set sidebar title
st.sidebar.title('Settings')
st.sidebar.write('Atur dashboard melalui pengaturan di bawah')\

# Adding sidebar and selectbox for scatter plot axis
x_axis= st.sidebar.selectbox(
    'X-axis',
    ['box_office', 'budget']
)
y_axis = st.sidebar.selectbox(
    'Y-axis',
    ['rating']
)

#Scatter plot
st.header("Scatter Plot")
st.subheader(f"Scatter Plot: {x_axis.title()} vs {y_axis.title()}")
fig = px.scatter(
    imdb_data,
    x=x_axis,
    y=y_axis,
    labels={x_axis: x_axis.title(), y_axis: y_axis.title()},
    hover_data=["name"],  # Show movie title on hover
)

st.plotly_chart(fig)

#Add filter by year (slider), filter by runtime to sidebar

#Add filter by year (slider)
# Define the range of years
start_year = 1921
end_year = 2022

# Add a slider for selecting a range of years
filter_by_year = st.sidebar.slider(
    'Filter by Year',
    min_value=start_year,
    max_value=end_year,
    value=(start_year, end_year),  # Default range
    step=1
)

#Add filter by run time 
filter_by_runtime= st.sidebar.selectbox(
    'Runtime',
    ["Up to 1.5 hours", "1.5 to 2 hours", "2 to 2.5 hours",
    "2.5 to 3 hours", "More than 3 hours"]
)


# Filtered table (based on filter on the sidebar)
filtered_data = imdb_data.copy()

runtime_mapping = {
    "Up to 1.5 hours": (0, 90),
    "1.5 to 2 hours": (90, 120),
    "2 to 2.5 hours": (120, 150),
    "2.5 to 3 hours": (150, 180),
    "More than 3 hours": (180, float("inf"))
}

runtime_min, runtime_max = runtime_mapping[filter_by_runtime]

filtered_data = filtered_data[(filtered_data["year"] >= filter_by_year[0]) &
                              (filtered_data["year"] <= filter_by_year[1])]

# Split genres and filter by runtime
filtered_data = filtered_data.assign(genre=filtered_data['genre'].str.split(",")).explode('genre')

st.header("Filtered Movies Table")
st.dataframe(filtered_data)

