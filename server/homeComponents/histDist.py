import matplotlib.pyplot as plt
import pandas as pd

#read in a csv file into a pandas dataframe
df = pd.read_csv('../data/data.csv')

#convert the 4* column dataframe into a numpy array
ratings = df['4*'].to_numpy()
print(ratings)

bin_edges = [i * 10 for i in range(11)]  # creates bins from 0 to 100 with step of 10

figsize_in_inches = (200/96, 200/96)

# Create the pie chart with the specified size
plt.figure(figsize=figsize_in_inches)
plt.hist(ratings, bins=bin_edges, edgecolor='black')
plt.title('Distribution of 4* ratings')
plt.xlabel('Percentage Score')
plt.ylabel('Number of Submissions')

plt.savefig('histDist.png')