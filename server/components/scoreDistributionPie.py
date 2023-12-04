import pandas as pd
import matplotlib.pyplot as plt
import mpld3

# Load data
file_path = '..\data\data.csv'  # Replace with your CSV file path
df = pd.read_csv(file_path)

# Calculate the sum of all the star ratings
ratings = df[['4*', '3*', '2*', '1*']].sum()

# Create the pie chart
fig, ax = plt.subplots()
ax.pie(ratings, labels=ratings.index, autopct='%1.1f%%', startangle=90)
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.title('Distribution of Star Ratings')

# Save the plot as an HTML file using mpld3
mpld3.save_html(fig, 'star_ratings_distribution.html')
