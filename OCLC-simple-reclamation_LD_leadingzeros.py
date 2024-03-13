import pandas as pd
from pathlib import Path

# this script is working with ART-testfile-scrubbed but not so much with the Alma set. Did I misformat at some step?

# Define input and output directories
input_dir = Path("C:/Users/lmd8/OneDrive - Rice University/Desktop/testing/")
output_dir = Path("C:/Users/lmd8/OneDrive - Rice University/Desktop/testing/")

print("Starting...")

# Function to normalize identifier by removing non-numeric characters and leading zeros
def normalize_identifier(identifier):
    # Remove non-numeric characters
    identifier = ''.join(filter(str.isdigit, str(identifier)))
    # Ensure all identifiers have the same length by padding with leading zeros
    return identifier.zfill(10)  # Assuming maximum length is 10 characters

# Read the files
try:
    ALMAdf = pd.read_csv(input_dir / "ART-testfile-scrubbed.txt", sep='\t')
    OCLCdf = pd.read_csv(input_dir / "OCLC-merged-original.txt", sep='\t')
except FileNotFoundError as e:
    print("Error: Input file(s) not found.")
    exit()  # Terminate script

# Normalize the identifiers in both dataframes
ALMAdf['Normalized_ID'] = ALMAdf['035$a'].apply(normalize_identifier)
OCLCdf['Normalized_ID'] = OCLCdf['001'].apply(normalize_identifier)

# Find unmatched
NotInOCLC = ALMAdf[~ALMAdf['Normalized_ID'].isin(OCLCdf['Normalized_ID'])]
NotInAlma = OCLCdf[~OCLCdf['Normalized_ID'].isin(ALMAdf['Normalized_ID'])]

# Save results to TXT (TSV)
NotInOCLC.to_csv(output_dir / "NotInOCLC.txt", sep='\t', index=False, columns=['001', '035$a'])
NotInAlma.to_csv(output_dir / "NotInALMA.txt", sep='\t', index=False, columns=['001'])

# Print completion message
print("Finished. Check output files.")
