import pandas as pd
import os

# Global Variables
OUTPUT_EXTENSION = '.csv'
INPUT_EXTENSION = '.txt'
INPUT_FOLDER = 'C:/Users/Documents/New folder/Input/'
OUTPUT_FOLDER = 'C:/Users/Documents/New folder/Output/'


# Function to read the Text Files
def read_text_file(input_file):
    file_path = os.path.join(INPUT_FOLDER, input_file)
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            data.append(line.strip())
    return data


# This function will remove the first and last line from the text file
def remove_first_last_rows(data):
    return data[1:-1]  # Remove first and last rows


# This function will remove the unwanted quotes and commas from the text file
def strip_quotes(data):
    for i in range(len(data)):
        data[i] = data[i].strip('"').rstrip('",')  # Strip quotes and '",' from each line
    return data


# This function will split the data into each column
def split_data(data):
    split_data_rows = []
    for line in data:
        columns = line.split('","')  # Split on '","' pattern
        split_data_rows.append(columns)
    return split_data_rows


# This function creates a dataframe from the data we get
def create_dataframe(data):
    dataframe = pd.DataFrame(data)
    # Add a single quote to values in the 5th column
    dataframe.iloc[:, 4] = "'" + dataframe.iloc[:, 4].astype(str)
    # Add a single quote to values in the 6th column
    dataframe.iloc[:, 5] = "'" + dataframe.iloc[:, 5].astype(str)
    return dataframe


# This function removes the empty column
def remove_empty_columns(dataframe):
    dataframe = dataframe.replace('', pd.NA)  # Replace empty cells with NA
    dataframe = dataframe.dropna(axis=1, how='all')  # Remove empty columns
    dataframe = dataframe.loc[:, (dataframe.astype(bool)).any(axis=0)]  # Remove columns with all False/empty values
    return dataframe


# This function is to write DataFrame to a CSV file
def write_csv_file(dataframe, output_file):
    output_path = os.path.join(OUTPUT_FOLDER, output_file)
    dataframe.to_csv(output_path, index=False)
    print(f"Data successfully written to '{output_path}'.")
    try:
        with open(output_path, 'r') as file:
            print("Done!")
    except IOError:
        print("An error occurred while opening the file.")


# Main Call function
def main():
    input_files = os.listdir(INPUT_FOLDER)
    for input_file in input_files:
        if input_file.endswith(INPUT_EXTENSION):
            input_file_name = os.path.splitext(input_file)[0]
            print(f"Processing input file: {input_file_name}")
            data = read_text_file(input_file)
            data = remove_first_last_rows(data)
            data = strip_quotes(data)
            data = split_data(data)
            dataframe = create_dataframe(data)
            dataframe = remove_empty_columns(dataframe)
            
            output_file_name = input("Enter the output file name (without extension): ").upper()
            output_file = output_file_name + OUTPUT_EXTENSION
            
            write_csv_file(dataframe, output_file)
            print()
            

# Main function trigger / Program start
if __name__ == '__main__':
    main()
