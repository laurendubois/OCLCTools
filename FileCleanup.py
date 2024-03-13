import re

# Define the path to your input and output files
input_file_path = 'C:/Users/lmd8/OneDrive - Rice University/Desktop/testing/ART.txt'
output_file_path = 'C:/Users/lmd8/OneDrive - Rice University/Desktop/testing/ART_v2.txt'

# Open the input file for reading and the output file for writing
with open(input_file_path, 'r') as infile, open(output_file_path, 'w') as outfile:
    # Iterate through each line in the input file
    for index, line in enumerate(infile):
        # Skip processing the first row and copy it directly to the output file
        if index == 0:
            outfile.write(line)
            continue

        # Split the line by tab to separate the two quoted parts
        parts = line.strip().split('\t')
        if len(parts) == 2:
            # Extract the first part (number starting with "991...")
            first_part = parts[0].strip().strip('"')
            # Find and extract the OCoLC number in the second part
            ocolc_part = re.search(r'\(OCoLC\)(\w*\d+)', parts[1])
            if ocolc_part:
                ocolc_number = ocolc_part.group(1).strip().strip('"').lstrip('ocn').lstrip('on') # does not account for ocm, but when added turns IDs to floats
            else:
                ocolc_number = "0"
            # Write the processed line to the output file
            outfile.write(f'"{first_part}"\t"{ocolc_number}"\n')
        else:
            # If the line does not contain two parts, write it directly to the output file
            outfile.write(line)

print("Processing complete. Check the output file for results.")
