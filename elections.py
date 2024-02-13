import requests

ELECTIONS_URL = "https://www.googleapis.com/civicinfo/v2/elections"

VOTER_INFO_URL = "https://www.googleapis.com/civicinfo/v2/voterinfo"


API_KEY = 'AIzaSyD7UHjJIyPZzYUlGMrR858pk75hggjchMc'

def elections(api_key):
    """Queries the electionQuery endpoint with the provided API key"""

    query_params = {"key": api_key}
    api_response = requests.get(ELECTIONS_URL, params=query_params, timeout=300)
    print(api_response)
    print(api_response.reason)
    return api_response


def voter_info(api_key, address, election_id=None, official_only=False):
    """Queries the voterInfoQuery endpoint with the provided parameters"""

    query_params = {"key": api_key, "address": address, "officialOnly": official_only}
    # Check for paramater validity
    if not isinstance(official_only, bool):
        raise ValueError("official_only must be True or False")

    if election_id:
        query_params["electionId"] = election_id

    api_response = requests.get(VOTER_INFO_URL, params=query_params, timeout=300)
    print(api_response)
    print(api_response.reason)
    return api_response

elections(API_KEY)