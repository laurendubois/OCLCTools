import json
import os
import pandas as pd
from bookops_worldcat import WorldcatAccessToken, MetadataSession

# Defines a method of getting tokens with BookOps
# Separate creds file for security
# TO DO: improve pathing for creds file
def get_token():
    creds_fh = os.path.join(os.getenv("HOME"), "Documents/PycharmProjects/OCLCTools/my_wskey.json")
    with open(creds_fh, "r") as file:
        creds = json.load(file)
        token = WorldcatAccessToken(
            key=creds["key"],
            secret=creds["secret"],
            scopes=creds["scopes"],
            principal_id=creds["principal_id"],
            principal_idns=creds["principal_idns"],
            agent="de12@rice.edu"
        )
        return token

# Pandas can read a gsheet directly
# TO DO: Swap middle concat to a new sheet
gsheet = pd.read_csv(
    "https://docs.google.com/spreadsheets/d/"
    + "1INovWFSXIBgxKJIrixBD-LWIb_2DKZ6LhlB2P4Gx3Qc"
    + "/export?gid=0&format=csv"
)

# Creates a list of oclc IDs in memory to iterate over
# Formally requests a token via OCLC API
oclc_numbers = [o for o in gsheet["OCLCID"]]
token = get_token()

# Loop over the above oclc numbers and act on them
with MetadataSession(authorization=token, agent="de12@rice.edu") as session:

    for o in oclc_numbers:
        # !!Create an exception wrapper
        # Preview through matchMARC should minimize errors
        response = session.holding_get_status(oclcNumber=o)
        print(response.json())
        #response2 = session.holding_unset(oclcNumber=o)
        #print(response2)
