import json
from bookops_worldcat import WorldcatAccessToken, MetadataSession


def get_token():
    creds_fh = "my_wskey.json"
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


def main():
    token = get_token()
    if token:
        print(token)
        print(token.is_expired())

        # Read OCLC numbers from a text file
        with open('oclc_ids.txt', 'r') as f:
            oclc_numbers = [line.strip() for line in f]

        for oclc_number in oclc_numbers:
            with MetadataSession(authorization=token) as session:
                try:
                    response_get_current = session.holdings_get_current(oclcNumbers=[oclc_number])
                    print(f"Old Response for {oclc_number} = {response_get_current.json()['holdings'][0]['holdingSet']}")

                    session.holdings_set(oclcNumber=oclc_number)

                    response_get_current_after_set = session.holdings_get_current(oclcNumbers=[oclc_number])
                    print(f"New Response for {oclc_number} = {response_get_current_after_set.json()['holdings'][0]['holdingSet']}\n")

                except Exception as e:
                    print(f"An error occurred during MetadataSession call: {e}")


if __name__ == "__main__":
    main()