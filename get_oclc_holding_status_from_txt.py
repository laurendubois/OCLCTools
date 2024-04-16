import json
# import pandas as pd only needed for CSV/XLS
from bookops_worldcat import WorldcatAccessToken, MetadataSession

# This reads a txt of oclc ids and returns our holding status

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


# Read OCLCID numbers from a text file
txt_file_path = "oclc_list.txt"
oclc_numbers = []
with open(txt_file_path, "r") as txt_file:
    for line in txt_file:
        oclc_numbers.append(line.strip())

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
            responses_list.append({'OCLCID': o, 'holdingCurrentlySet': holding_value})
        except Exception as e:
            errors_list.append({"OCLCID": o, "Error": str(e)})

# Write the data to text files
with open('oclc_list_output.txt', 'w') as results_file:
    for item in responses_list:
        results_file.write(
            f"{item['OCLCID']}|{item['holdingCurrentlySet']}\n"
        )

with open('oclc_list_errors.txt', 'w') as errors_file:
    for item in errors_list:
        errors_file.write(
            f"OCLCID: {item['OCLCID']}|Error: {item['Error']}\n"
        )

print('Output files saved as oclc_status_output.txt and oclc_status_errors.txt.')
