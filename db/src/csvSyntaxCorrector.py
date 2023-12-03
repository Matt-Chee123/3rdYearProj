import csv

csv_path = 'C:/Users/Razer/OneDrive/zY3 Uni/3rd year project/ThirdYearProject/db/data/data_withoutHeaders.csv'

output_csv_file = '../data/output.csv'
# Open the CSV file
with open(csv_path, 'r', newline='') as infile, open(output_csv_file, 'w', newline='') as outfile:
    csv_reader = csv.reader(infile)
    csv_writer = csv.writer(outfile)

    # Iterate through each row in the input CSV file
    for row in csv_reader:
        # Check if the record is related to "Computer Science and Informatics"
        if row[5] == 'Computer Science and Informatics':
            # Replace empty fields with 'NULL'
            cleaned_row = ['NULL' if field == '' else field for field in row]

            # Write the cleaned row to the output CSV file
            csv_writer.writerow(cleaned_row)