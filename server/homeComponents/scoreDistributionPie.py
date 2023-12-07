import pandas as pd
import matplotlib.pyplot as plt

# load data
file_path = '..\data\data.csv'
df = pd.read_csv(file_path)

# calculate sum of all the star ratings
ratings = df[['4*', '3*', '2*', '1*']].sum()

# set the size of the image
figsize_in_inches = (200/96, 200/96)

# create the pie chart with specified size
plt.figure(figsize=figsize_in_inches)
plt.pie(ratings, labels=ratings.index, autopct='%1.1f%%', startangle=90)
plt.axis('equal')  # equal aspect ratio ensures that pie is drawn as a circle.
plt.title('Distribution of Star Ratings')

# save the plot as a PNG image
plt.savefig('star_ratings_distribution.png', bbox_inches='tight', dpi=96)
plt.close()
