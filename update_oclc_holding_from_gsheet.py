import json
import pandas as pd
from bookops_worldcat import WorldcatAccessToken, MetadataSession
from bookops_worldcat.errors import WorldcatRequestError

# Defines a method of getting tokens with BookOps
# Separate creds file for security
# TO DO: improve pathing for creds file
def get_token():
    creds_fh = r"C:\Users\lmd8\PycharmProjects\OCLCTools\my_wskey.json"  # Use raw string to handle backslashes
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
# TO DO: Swap middle concat to a new sheet
gsheet = pd.read_csv(
    "https://docs.google.com/spreadsheets/d/"
    + "1INovWFSXIBgxKJIrixBD-LWIb_2DKZ6LhlB2P4Gx3Qc"
    + "/export?gid=0&format=csv"
)
# Creates a list of OCLC IDs in memory to iterate over
# Formally requests a token via OCLC API
oclc_numbers = [o for o in gsheet["OCLCID"]]
token = get_token()

# Loop over the above OCLC numbers and act on them
with MetadataSession(authorization=token, agent="lmd8@rice.edu") as session:
    for o in oclc_numbers:
        try:
            # Attempt to set the holding for the current OCLC number
            response = session.holding_set(oclcNumber=o)
            print(f"Successfully set holding for OCLC ID: {o}")
        except WorldcatRequestError as e:
            # If an error occurs, print an informative message
            print(f"Error occurred while setting holding for OCLC ID {o}:")
            print(f"Error code: {e.code}, Error message: {e.message}")
        except Exception as e:
            # Catch any other unexpected exceptions
            print(f"An unexpected error occurred while setting holding for OCLC ID {o}:")
            print(e)