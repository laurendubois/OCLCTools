import pandas as pd
from pathlib import Path

# Locate the files
# downloads_path = Path("C:/Users/lmd8/OneDrive - Rice University/Desktop/testing")

# Read the files
# ALMAdf = pd.read_csv(downloads_path / "ART_v3.txt", sep='\t', dtype=str)
# OCLCdf = pd.read_csv(downloads_path / "OCLC.txt", sep='\t', dtype=str)

# Read the files
ALMAdf = pd.read_csv("C:/Users/lmd8/OneDrive - Rice University/Desktop/testing/ART_testfile.txt", sep='\t')
OCLCdf = pd.read_csv("C:/Users/lmd8/OneDrive - Rice University/Desktop/testing/OCLC.txt", sep='\t')


# Print some values in the DataFrames to ensure data was read correctly
print("ALMAdf head:")
print(ALMAdf.head())
print("OCLCdf head:")
print(OCLCdf.head())

# Generalized extraction of numeric patterns, treating each number as a string
def extract_numeric(df, col_name):
    # This function will extract all numeric sequences from the specified column and return them
    df[col_name] = df[col_name].str.extractall(r'(\d+)').groupby(level=0).apply(lambda x: '|'.join(x[0])).astype(str)

# Apply the function to each relevant column in both DataFrames
extract_numeric(ALMAdf, '035$a')
extract_numeric(OCLCdf, '001')

# find unmatched
NotInOCLC = ALMAdf[~ALMAdf['035$a'].isin(OCLCdf['001'])]
NotInAlma = OCLCdf[~OCLCdf['001'].isin(ALMAdf['035$a'])]

# Save results to TXT (TSV)
NotInOCLC.to_csv("C:/Users/lmd8/OneDrive - Rice University/Desktop/testing/NotInOCLC.txt", sep='\t', index=False, columns=['001', '035$a'])
NotInAlma.to_csv("C:/Users/lmd8/OneDrive - Rice University/Desktop/testing/NotInALMA.txt", sep='\t', index=False, columns=['001'])

print("ALMAdf['035$a'] values:")
print(ALMAdf['035$a'])

print("OCLCdf['001'] values:")
print(OCLCdf['001'])

# Print completion message
print("Process complete. Check output file.")