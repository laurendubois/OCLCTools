import os

# I believe this merged the separate OCLC exports but need to revisit later to confirm

# Path to the directory containing tab-separated text files
directory = 'C:/Users/lmd8/OneDrive - Rice University/Desktop/testing/original-alma'

# Output file name for merged content with .txt extension
output_file = os.path.join(directory, 'ALMA-merged.txt')

# Function to merge tab-separated text files
def merge_tab_separated_files(directory, output_file):
    with open(output_file, 'w', newline='') as outfile:
        # Iterate through each file in the directory
        for filename in os.listdir(directory):
            if filename.endswith(".txt"):  # Assuming all files are tab-separated text files
                with open(os.path.join(directory, filename), 'r', newline='') as infile:
                    # Write the content of each file to the output file
                    outfile.write(infile.read())

# Merge tab-separated text files
merge_tab_separated_files(directory, output_file)

print(f"All tab-separated text files in {directory} have been merged into {output_file}.")
