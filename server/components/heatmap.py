import pandas as pd
import folium
from folium.plugins import HeatMap, MarkerCluster

# Read data from CSV file
file_path = '..\data\data.csv'  # Replace with your CSV file path
df = pd.read_csv(file_path)

# Calculate weighted averages
df['Weighted Average'] = (4 * df['4*'] + 3 * df['3*'] + 2 * df['2*'] + 1 * df['1*']) / 100

# Create a base map
map = folium.Map(location=[55.3781, -3.4360], zoom_start=6)  # Coordinates roughly at the center of the UK

# Create a HeatMap data
heat_data = [[row['Latitude'], row['Longitude'], row['Weighted Average']] for index, row in df.iterrows()]
# Add the heat map layer
HeatMap(heat_data).add_to(map)

# Create a MarkerCluster object
marker_cluster = MarkerCluster().add_to(map)

for index, row in df.iterrows():
    # Create a marker with popup
    popup_content = f"""<b>Location:</b> {row['Institution name']}<br>
                        <b>Environment Score:</b> {row['Weighted Average']}<br>"""  # Replace 'some_info_column' with your column name
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=folium.Popup(popup_content, max_width=300,min_width=100),
        icon=None  # This will use the default icon
    ).add_to(marker_cluster)

# Save to an HTML file
map.save('uk_heatmap.html')
