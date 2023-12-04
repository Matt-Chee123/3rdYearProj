import pandas as pd

# Load data
file_path = '..\data\data.csv'  # Replace with your CSV file path
df = pd.read_csv(file_path)

# Define a function to calculate the score
def calculate_score(row):
    # Assuming the ratings are out of 100 and the higher the better
    score = row['4*'] * 4 + row['3*'] * 3 + row['2*'] * 2 + row['1*']
    return score

# Calculate score for each record
df['Score'] = df.apply(calculate_score, axis=1)

# Sort the DataFrame based on the score in descending order
df_sorted = df.sort_values(by='Score', ascending=False)

# Save the sorted DataFrame to a new CSV if needed
df_sorted.to_csv('../data/sorted_data.csv', index=False)
