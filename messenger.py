# API call code adapted from Github
# URL: https://github.com/k0pak4/google-civic-information-api-py/tree/main/src/google_civic_information_api
# Author: k0pak4
# Accessed 2/6/24

# Server in Python
# Binds REP socket to tcp://*:2121
# Expects b"[address]"" from client, replies with b"World"
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


VALID_LEVELS = ["administrativeArea1", "administrativeArea2", "country",
                "international", "locality", "regional", "special", "subLocality1", "subLocality2"]

VALID_ROLES = ["deputyHeadOfGovernment", "executiveCouncil", "governmentOfficer", "judge",
               "headOfGovernment", "headOfState", "highestCourtJudge", "legislatorLowerBody",
               "legislatorUpperBody", "schoolBoard", "specialPurposeOfficer"]


officials = []
index = 0

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


def format_data(json_object):
    pass


# keys = normalizedInput, kind, divisions, offices, officials
# keys in officals: name, address, party, phones, urls, photoURL, channels, 
def sort_officals(data, officals_list):
    counter = 0
    #Only works if levels == 'country':
    if 'offices' in data:
        senator_counter = False
        #print('test\n')
        for x in range(len(data['officials'])):
            # print(data['officials'][x]['name'])
            # print(data['officials'][x]['phones'][0])
            address_data = data['officials'][x]['address'][0]
            return_address = address_data['line1'] + ' '+ address_data['city'] + ', ' + address_data['state'] + ' ' + address_data['zip']
            # print(return_address)
            # print(data['officials'][x]['urls'][0])
            # print(data['officials'][x]['party'])
            offical = Offical(data['offices'][counter]['name'], data['officials'][x]['name'], data['officials'][x]['phones'][0], return_address, data['officials'][x]['urls'][0], data['officials'][x]['party'])
            officals_list.append(offical)
            if data['offices'][counter]['name'] == 'U.S. Senator' and senator_counter == False:
                counter -=1
                senator_counter = True
            counter += 1
        



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
    # Waits for next request from client (recived as bytes object)
    input_address = socket.recv()
    print(f"Recieved a request: {input_address}")

    # Calls API and gets json object
    officals_list = []
    r = representative_info_by_address(API_KEY, input_address, include_offices=True, levels='country')
    data = r.json()

    #Send reply to client
    if r.status_code != 200:
        response_string = "An error occured, please try a different address"
        print(r.text)

    if r.status_code == 200:
        response_string = ''
        sort_officals(data, officals_list)
        for offical in officals_list:
            #print(offical.get_contact_info())
            response_string += offical.get_contact_info() + '\n\n'

    #print(response_string)
    #Send reply to client
    socket.send_string(f"{response_string}")
