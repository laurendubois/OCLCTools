import pandas as pd
from pathlib import Path

# Define input and output directories
input_dir = Path("C:/Users/lmd8/OneDrive - Rice University/Desktop/testing/")
output_dir = Path("C:/Users/lmd8/OneDrive - Rice University/Desktop/testing/")

# Read the files
try:
    ALMAdf = pd.read_csv(input_dir / "ART-testfile-scrubbed.txt", sep='\t')
    OCLCdf = pd.read_csv(input_dir / "OCLC-merged-original.txt", sep='\t')
except FileNotFoundError as e:
    print("Error: One or more input files not found.")
    exit()  # Terminate script execution if files are not found

# Generalized extraction of numeric patterns, treating each number as a string
def extract_numeric(df, col_name):
    # Extract all numeric sequences from the specified column and return them
    df[col_name] = df[col_name].str.extractall(r'(\d+)').groupby(level=0).apply(lambda x: '|'.join(x[0])).astype(str)

# Apply the function to each relevant column in both DataFrames
extract_numeric(ALMAdf, '035$a')
extract_numeric(OCLCdf, '001')

# Find unmatched
NotInOCLC = ALMAdf[~ALMAdf['035$a'].isin(OCLCdf['001'])]
NotInAlma = OCLCdf[~OCLCdf['001'].isin(ALMAdf['035$a'])]

# Save results to TXT (TSV)
NotInOCLC.to_csv(output_dir / "NotInOCLC.txt", sep='\t', index=False, columns=['001', '035$a'])
NotInAlma.to_csv(output_dir / "NotInALMA.txt", sep='\t', index=False, columns=['001'])

# Print completion message
print("Finished. Check output files.")
