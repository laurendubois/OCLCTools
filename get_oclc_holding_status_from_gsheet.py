import json
import pandas as pd
from bookops_worldcat import WorldcatAccessToken, MetadataSession

# This will read a Google Sheet list and report current OCLC holding status using the API
# Output is MMS ID / OCLC ID pairs


# Defines a method of getting tokens with BookOps
# Separate creds file for security
def get_token():
    creds_fh = "C:/Users/lmd8/PycharmProjects/OCLCTools/my_wskey.json"
    with open(creds_fh, "r") as file:
        creds = json.load(file)
        token = WorldcatAccessToken(
            key=creds["key"],
            secret=creds["secret"],
            scopes=creds["scopes"],
            principal_id=creds["principal_id"],
            principal_idns=creds["principal_idns"],
            agent="lmd8@rice.edu"
        )
        return token

# Pandas can read a gsheet directly
gsheet = pd.read_csv(
   "https://docs.google.com/spreadsheets/d/"
   + "1INovWFSXIBgxKJIrixBD-LWIb_2DKZ6LhlB2P4Gx3Qc"
   + "/export?gid=0&format=csv"
)

# Creates a list of OCLC IDs in memory to iterate over
oclc_mms_mapping = {}  # Dictionary to store OCLC to MMS ID mapping
oclc_numbers = gsheet["OCLCID"].tolist()  # Convert OCLCID column to a list

for index, row in gsheet.iterrows():
    oclc_mms_mapping[row['OCLCID']] = str(row['MMSID'])

# Request token via OCLC API
token = get_token()

# List to store responses and errors
responses_list = []
errors_list = []

# Loop over the OCLC numbers and act on them
with MetadataSession(authorization=token, agent="lmd8@rice.edu") as session:
    for index, o in enumerate(oclc_numbers, start=1):
        try:
            response = session.holding_get_status(oclcNumber=o)
            print(f"Response {index}: ", response.json())  # Print the response for debugging purposes with index
            holding_value = False
            if 'content' in response.json() and 'holdingCurrentlySet' in response.json()['content']:
                holding_value = response.json()['content']['holdingCurrentlySet']
            responses_list.append({'OCLCID': o, 'MMSID': oclc_mms_mapping.get(o), 'holdingCurrentlySet': holding_value})
        except Exception as e:
            errors_list.append({"OCLCID": o, "MMSID": oclc_mms_mapping.get(o), "Error": str(e)})

# Write the data to text files
with open('holding_status_output.txt', 'w') as results_file:
    for item in responses_list:
        results_file.write(
            f"OCLCID: {item['OCLCID']}|MMSID: {item['MMSID']}|Holding: {item['holdingCurrentlySet']}\n"
        )

with open('holding_status_errors.txt', 'w') as errors_file:
    for item in errors_list:
        errors_file.write(
            f"OCLCID: {item['OCLCID']}|MMSID: {item['MMSID']}|Error: {item['Error']}\n"
        )

print('Output files saved as holding_status_output.txt and holding_status_errors.txt.')
