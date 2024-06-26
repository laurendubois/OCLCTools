import pandas as pd
from pathlib import Path

# Compares two files to report what is not in both

# Define input and output directories
input_dir = Path("C:/Users/lmd8/OneDrive - Rice University/Desktop/testing/")
output_dir = Path("C:/Users/lmd8/OneDrive - Rice University/Desktop/testing/")


def normalize_identifier(identifier):
    """Function to normalize identifier by removing non-numeric characters and correcting leading zeros"""
    identifier = ''.join(filter(str.isdigit, str(identifier)))

    # Ensure all identifiers have the same length by padding with leading zeros
    return identifier.zfill(12)  # Assuming maximum length is 12 characters


# Read the files
# Added parameter \t due to errors, then added dtype after errors
try:
    ALMAdf = pd.read_csv(input_dir / "ALMA-cleaned-test.txt", sep='\t', dtype='unicode')
    OCLCdf = pd.read_csv(input_dir / "OCLC-merged-test.txt", sep='\t', dtype='unicode')
except FileNotFoundError as e:
    print("Error: Input file(s) not found.")
    exit()  # Terminate script

# Normalize the identifiers in both DF
ALMAdf['Normalized_ID'] = ALMAdf['035$a'].apply(normalize_identifier)
OCLCdf['Normalized_ID'] = OCLCdf['001'].apply(normalize_identifier)

# Find unmatched
NotInOCLC = ALMAdf[~ALMAdf['Normalized_ID'].isin(OCLCdf['Normalized_ID'])]
NotInAlma = OCLCdf[~OCLCdf['Normalized_ID'].isin(ALMAdf['Normalized_ID'])]

# Print the data values in both DF
print("Example data values being compared in 'NotInOCLC' dataframe:")
print(NotInOCLC[['Normalized_ID', '035$a']])

print("\nExample data values being compared in 'NotInAlma' dataframe:")
print(NotInAlma[['Normalized_ID', '001']])

# Save results to TXT (TSV)
NotInOCLC.to_csv(output_dir / "alma_not_found_in_oclc_file.txt", sep='\t', index=False, columns=['001', '035$a'])
NotInAlma.to_csv(output_dir / "oclc_not_found_in_alma_file.txt", sep='\t', index=False, columns=['001'])

# Print completion message
print("Finished - check output files.")
