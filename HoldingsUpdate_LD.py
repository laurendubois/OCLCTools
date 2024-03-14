import json
import pandas as pd
from bookops_worldcat import WorldcatAccessToken, MetadataSession

# This will read a Google Sheet list and tell us our current OCLC holding status using the API
# Defines a method of getting tokens with BookOps
# Separate creds file for security
def get_token():
    creds_fh = "C:/Users/lmd8/PycharmProjects/OCLCTools/Worldcat-API/my_wskey.json"
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

# Creates a list of oclc IDs in memory to iterate over
# Formally requests a token via OCLC API
oclc_mms_mapping = {}  # Dictionary to store OCLC to MMS ID mapping
oclc_numbers = [o for o in gsheet["OCLCID"]]  # List comprehension to get OCLC numbers from the sheet

for index, row in gsheet.iterrows():
    oclc_mms_mapping[row['OCLCID']] = str(row['MMSID'])

token = get_token()

# List to store responses and errors
responses_list = []
errors_list = []

# Loop over the above OCLC numbers and act on them
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

# Convert the list of responses into a DataFrame
responses_df = pd.DataFrame(responses_list)
errors_df = pd.DataFrame(errors_list)

# Write the DataFrame to a CSV file
responses_df.to_csv('HoldingsUpdate_results.csv', index=False)
errors_df.to_csv('HoldingsUpdate_errors.csv', index=False)

print('Finished - check output files.')
