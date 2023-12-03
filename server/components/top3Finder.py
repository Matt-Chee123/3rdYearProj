import pandas as pd

data = pd.read_csv('../../db/data/data.csv', encoding='cp1252')
print(data)

filtered_data = data[
    (data['Profile'] == 'Environment') &
    (data['Unit of assessment name'].str.contains('Computer Science and Informatics', na=False))
    ]

def calculate_weighted_average(df):
    # Convert the '1*', '2*', '3*', and '4*' columns to numeric
    star_columns = ['1*', '2*', '3*', '4*']
    for col in star_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Calculate the weighted average for each row
    df['Weighted Average'] = (df['1*'] * 1 + df['2*'] * 2 + df['3*'] * 3 + df['4*'] * 4)

    # Normalize the weighted average by the sum of the percentages
    df['Weighted Average'] /= df[star_columns].sum(axis=1)

    # Sort the DataFrame by the new 'Weighted Average' column
    df_sorted = df.sort_values(by='Weighted Average', ascending=False)

    # Get the top 3 and bottom 3 weighted averages
    top_3 = df_sorted.head(3)
    bottom_3 = df_sorted.tail(3)

    # Return the top 3 and bottom 3 as a tuple of DataFrames
    return top_3, bottom_3

# Assume 'df' is your DataFrame loaded from the CSV
# Call the function and get the top and bottom 3
top_3, bottom_3 = calculate_weighted_average(filtered_data)

# Output the results
# Output the results
print("Top 3 Weighted Averages:")
print(top_3[['Institution name', 'Weighted Average']])

print("\nBottom 3 Weighted Averages:")
print(bottom_3[['Institution name', 'Weighted Average']])