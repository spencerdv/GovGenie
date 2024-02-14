# API call code adapted from Github
# URL: https://github.com/k0pak4/google-civic-information-api-py/tree/main/src/google_civic_information_api
# Author: k0pak4
# Accessed 2/6/24

# Server in Python
# Binds REP socket to tcp://*:21213
import os
from dotenv import load_dotenv
import time
import zmq
import requests

# For testing any bugs with ZeroMQ:
# print(f"Current libzmq version is {zmq.zmq_version()}")
# print(f"Current  pyzmq version is {zmq.__version__}")

# Google API key
load_dotenv(override=True)
API_KEY = os.getenv('API_KEY')
include_offices = {}

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:21213")

url = 'https://www.googleapis.com/civicinfo/v2/representatives'
#REPS_URL = "https://www.googleapis.com/civicinfo/v2/representatives?key="


VALID_LEVELS = ["country", "administrativeArea1", "administrativeArea2", "locality"]

# "Regional, locality, international, subLocality1, subLocality2" are valid levels but return nothing
# adminstriativeArea1 does state officals and college trustees
# adminstriativeArea2 does covers county officals

VALID_ROLES = ["deputyHeadOfGovernment", "executiveCouncil", "governmentOfficer", "judge",
               "headOfGovernment", "headOfState", "highestCourtJudge", "legislatorLowerBody",
               "legislatorUpperBody", "schoolBoard", "specialPurposeOfficer"]



class Offical():
    def __init__(self, title, name, phone, address, website, party):
        self.title = title
        self.name = name
        self.phone = phone
        self.address = address 
        self.website = website
        self.party = party
    
    def get_contact_info(self):
        return (self.title + ' | ' + self.name  + ' | ' + self.phone + ' | ' + self.address + ' | ' + self.party + ' | ' + self.website)


def format_bill(json_object):
    pass

# keys = normalizedInput, kind, divisions, offices, officials
# keys in officals: name, address, party, phones, urls, photoURL, channels, 
def sort_officals(data, officals_list):
    state_string = 'ocd-division/country:us/state:'
    state = data['normalizedInput']['state'].lower()
    counter = 0
    if 'offices' in data:
        new_list =[]
        title_list = []
        for iteration in range(len(data['offices'])):
            new_list.append(data['offices'][iteration]['officialIndices'])

        for office in range(len(data['offices'])):
            title_list.append(data['offices'][office]['name'])
        
        for iteration in range(len(data['officials'])):
            count = 0
            for inner_list_count in range(len(new_list)):
                if iteration in new_list[inner_list_count]:
                    title = title_list[count]
                    break
                count += 1
            
            phone = 'Phone not public'
            return_address = 'Address not public'
            website = 'No website available'
            party = 'Party not public'
            
            name = data['officials'][iteration]['name']
            if 'phones' in data['officials'][iteration]:
                phone = (data['officials'][iteration]['phones'][0])
            if 'address' in data['officials'][iteration]:
                address_data = data['officials'][iteration]['address'][0]
                return_address = address_data['line1'] + ' '+ address_data['city'] + ', ' + address_data['state'] + ' ' + address_data['zip']
            if 'urls' in data['officials'][iteration]:
                website = data['officials'][iteration]['urls'][0]
            if 'party' in data['officials'][iteration]:
                party = data['officials'][iteration]['party']
            offical = Offical(title, name, phone, return_address, website, party)
            officals_list.append(offical)
        

def representative_info_by_address(api_key, address, include_offices=True, levels=None, roles=None):
    """Queries the representativeInfoByAddress endpoint with provided parameters"""

    query_params = {"key": api_key, "address":address, "includeOffices": include_offices}

    # Check for paramater validity
    if not isinstance(include_offices, bool):
        raise ValueError("include_offices must be True or False")
    if levels and levels in VALID_LEVELS:
        query_params["levels"] = levels
    elif levels and levels not in VALID_LEVELS:
        raise ValueError(f"levels must be one of {VALID_LEVELS}")
    if roles and roles in VALID_ROLES:
        query_params["roles"] = roles
    elif roles and roles not in VALID_ROLES:
        raise ValueError(f"roles must be one of {VALID_ROLES}")

    api_response = requests.get(url, params=query_params)

    return api_response


while True:
    officals_list = []
    # Waits for next request from client (recived as bytes object)
    input_address = socket.recv()
    print(f"Recieved a request: {input_address}")

    '''
    State/Federal select functionality
    time.sleep(10)
    level_input = socket.recv()
    level_input = level_input.decode
    print(f"Recieved a response: {level_input}")

    #Calls API and gets json object    
    
    levels options include: "country", "administrativeArea1", "administrativeArea2", "locality". Will run all if no argument is passed for levels
    if level_input == 'all':
        r = representative_info_by_address(API_KEY, input_address, include_offices=True)
    elif level_input == 'federal':
        r = representative_info_by_address(API_KEY, input_address, include_offices=True, levels=["national"])
    elif level_input == 'state':
        r = representative_info_by_address(API_KEY, input_address, include_offices=True, levels=["administrativeArea1", "administrativeArea2"])
    '''
    r = representative_info_by_address(API_KEY, input_address, include_offices=True)
    data = r.json()

    #Send reply to client
    if r.status_code != 200:
        response_string = "An error occured, please try a different address."
        #print(r.text)

    if r.status_code == 200:
        response_string = ''
        sort_officals(data, officals_list)
        for offical in officals_list:
            response_string += offical.get_contact_info() + '\n\n'

    #Send reply to client
    socket.send_string(f"{response_string}")
