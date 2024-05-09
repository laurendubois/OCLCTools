import pandas as pd
import os

def read_oclc_numbers_from_file(file_path):
    with open(file_path, 'r') as file:
        # Strip leading zeros from each line (OCLC number) and add to a set
        return set(line.lstrip('0') for line in file.read().splitlines())

def compare_files(file1, directory_path):
    # Read OCLC numbers from file1, ignoring leading zeros
    oclc_numbers_file1 = read_oclc_numbers_from_file(file1)

    # Initialize a set to hold all OCLC numbers from the directory's files, ignoring leading zeros
    oclc_numbers_in_directory = set()

    # Iterate over all txt files in the given directory and aggregate their OCLC numbers
    for filename in os.listdir(directory_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory_path, filename)
            oclc_numbers_in_directory.update(read_oclc_numbers_from_file(file_path))

    # Find OCLC numbers in file1 that are missing in the directory's files
    missing_oclc_numbers = oclc_numbers_file1 - oclc_numbers_in_directory

    # Create a DataFrame from the missing OCLC numbers
    missing_df = pd.DataFrame(list(missing_oclc_numbers), columns=['Missing OCLC numbers'])

    return missing_df

if __name__ == "__main__":
    file1_path = r"C:\Users\lmd8\PycharmProjects\OCLCTools\CompareLists\test\merged_OCLC.txt"  # Update this path
    directory_path = r"C:\Users\lmd8\PycharmProjects\OCLCTools\CompareLists\test\Alma"  # Update this path

    # Compare file1 against all txt files in the specified directory
    result_df = compare_files(file1_path, directory_path)

    # Save the result DataFrame to a new Excel file
    result_df.to_excel("Missing_OCLC_Numbers.xlsx", index=False)

    print("Results appended and saved in Missing_OCLC_Numbers.xlsx.")
