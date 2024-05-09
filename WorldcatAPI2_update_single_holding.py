import json
from bookops_worldcat import WorldcatAccessToken, MetadataSession


def get_token():
    creds_fh = "C:/Users/lmd8/PycharmProjects/OCLCTools/my_wskey.json"
    try:
        with open(creds_fh, "r") as file:
            creds = json.load(file)
            token = WorldcatAccessToken(
                key=creds["key"],
                secret=creds["secret"],
                scopes=creds["scopes"],
                agent="lmd8@rice.edu"
            )
            return token
    except FileNotFoundError:
        print(f"Error: File '{creds_fh}' not found.")
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON in '{creds_fh}'.")
    except KeyError as e:
        print(f"Error: Key '{e}' not found in JSON.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


token = get_token()
print(token)
print(token.is_expired())


with MetadataSession(authorization=token) as session:
    response = session.holdings_get_current(oclcNumbers=['1646927'])
    print(response.json())

with MetadataSession(authorization=token) as session:
    response = session.holdings_set(oclcNumber=1646927)
    print(response.json())

with MetadataSession(authorization=token) as session:
    response = session.holdings_get_current(oclcNumbers=['1646927'])
    print(response.json())