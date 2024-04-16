import json
from bookops_worldcat import WorldcatAccessToken, MetadataSession

# This reads a txt of oclc ids to set or unset holding status

# Constants for file paths
OCLC_IDS_FILE = 'oclc_ids.txt'
OUTPUT_FILE = 'oclc_ids_output.txt'

def get_token():
    """Defines a method of getting tokens with BookOps"""
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


# Read OCLC IDs from the file
with open(OCLC_IDS_FILE, 'r') as file:
    oclc_numbers = [line.strip() for line in file]

# Get token for API access
token = get_token()

# Loop through the OCLC numbers and act on them
with open(OUTPUT_FILE, 'a') as output_file:
    for o in oclc_numbers:
        try:
            with MetadataSession(authorization=token, agent="lmd8@rice.edu") as session:
                # Unset holding below
                # session.holding_unset(oclcNumber=o)
                # Set holding below
                # session.holding_set(oclcNumber=o)
                # Get updated holding status
                api_response = session.holding_get_status(oclcNumber=o)
                if 'content' in api_response.json() and 'holdingCurrentlySet' in api_response.json()['content']:
                    holding_value = api_response.json()['content']['holdingCurrentlySet']
                else:
                    holding_value = None
                output_file.write(f"OCLCID: '{o}'|STATUS: {holding_value}\n")
        except Exception as e:
            output_file.write(f"OCLCID: '{o}'|ERROR: {str(e)}\n")
