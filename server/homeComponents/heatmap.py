import pandas as pd
import folium
from folium.plugins import HeatMap, MarkerCluster

# read data from CSV file
file_path = '..\data\data.csv'
df = pd.read_csv(file_path)

# calculate weighted averages
df['Weighted Average'] = (4 * df['4*'] + 3 * df['3*'] + 2 * df['2*'] + 1 * df['1*']) / 100

# create base map
map = folium.Map(location=[55.3781, -3.4360], zoom_start=6)

# create HeatMap data
heat_data = [[row['Latitude'], row['Longitude'], row['Weighted Average']] for index, row in df.iterrows()]
# add heat map layer
HeatMap(heat_data).add_to(map)

# create MarkerCluster layer
marker_cluster = MarkerCluster().add_to(map)

for index, row in df.iterrows():
    # create a marker with popup
    popup_content = f"""<b>Location:</b> {row['Institution name']}<br>
                        <b>Environment Score:</b> {row['Weighted Average']}<br>"""
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=folium.Popup(popup_content, max_width=300,min_width=100),
        icon=None
    ).add_to(marker_cluster)

# save to an HTML file
map.save('uk_heatmap.html')
