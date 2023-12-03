import folium
from folium.plugins import HeatMap
import pandas as pd
import numpy as np

# Define the place names, latitudes, and longitudes
place_names = [
    "University of Warwick, the UK",
    "University of Bristol, the UK",
    "London School of Economics and Political Science, the UK",
    "King's College London, the UK",
    "University of Manchester, the UK",
    "University of Cambridge, the UK"
]

latitudes = [
    52.379414,
    51.458447,
    51.514450,
    51.511448,
    53.466843,
    52.204311
]

longitudes = [
    -1.561904,
    -2.603288,
    -0.116674,
    -0.116414,
    -2.234597,
    0.113818
]

# Generate arbitrary weighted averages for these universities
# Using numpy to generate random numbers for demonstration purposes
weighted_averages = np.random.uniform(1, 5, size=len(place_names))

# Create the DataFrame
uni_df = pd.DataFrame({
    'Place Name': place_names,
    'Latitude': latitudes,
    'Longitude': longitudes,
    'Weighted Average': weighted_averages
})

# Display the DataFrame
print(uni_df)
# Assuming you have a DataFrame 'df' with 'latitude', 'longitude', and 'weighted_average' columns
# Create a base map
map = folium.Map(location=[55.3781, -3.4360], zoom_start=6)  # Coordinates roughly at the center of the UK

# Create a HeatMap data
heat_data = [[row['Latitude'], row['Longitude'], row['Weighted Average']] for index, row in uni_df.iterrows()]

# Add the heat map layer
HeatMap(heat_data).add_to(map)

# Save to an HTML file
map.save('uk_heatmap.html')
