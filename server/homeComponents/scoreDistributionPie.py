import pandas as pd
import matplotlib.pyplot as plt

# Load data
file_path = '..\data\data.csv'  # Replace with your CSV file path
df = pd.read_csv(file_path)

# Calculate the sum of all the star ratings
ratings = df[['4*', '3*', '2*', '1*']].sum()

# Set the size of the image - for example, 200x200 pixels
figsize_in_inches = (200/96, 200/96)  # Convert pixels to inches for Matplotlib

# Create the pie chart with the specified size
plt.figure(figsize=figsize_in_inches)
plt.pie(ratings, labels=ratings.index, autopct='%1.1f%%', startangle=90)
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.title('Distribution of Star Ratings')

# Save the plot as a PNG image
plt.savefig('star_ratings_distribution.png', bbox_inches='tight', dpi=96)
plt.close()
