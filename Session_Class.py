import json
import yelp_credentials
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from Cache_Class import *

yelp_session = False
data_cache = Cache('data.json')
token_cache = Cache('token.json')

class Session(object):
    
    CLIENT_ID = yelp_credentials.client_id
    CLIENT_SECRET = yelp_credentials.client_secret
    TOKEN_URL = 'https://api.yelp.com/oauth2/token'

    def __init__(self, token_dict = None):
        if token_dict:
            self.yelp_session = OAuth2Session(self.CLIENT_ID, token=token_dict)
        else:
            token_dict, self.yelp_session = self.get_new_token()

    def get_new_token(self):
        client = BackendApplicationClient(client_id=self.CLIENT_ID)
        yelp_session = OAuth2Session(client=client)
        token_dict = yelp_session.fetch_token(token_url=self.TOKEN_URL, client_id = self.CLIENT_ID, client_secret = self.CLIENT_SECRET)
        token_cache.set_in_cache('yelp', token_dict)
        return token_dict, yelp_session

    def get_data_from_api(self, ident, request_url, params_diction):
        # Call the get method on oauth instance
        resp = self.yelp_session.get(request_url,params=params_diction)
        # Get the string data and set it in the cache for next time
        data_str = resp.text
        data = json.loads(data_str)
        data_cache.set_in_cache(ident, data)
        return data



def create_request_identifier(url, params_diction):
    sorted_params = sorted(params_diction.items(),key=lambda x:x[0])
    params_str = "_".join([str(e) for l in sorted_params for e in l]) # Make the list of tuples into a flat list using a complex list comprehension
    total_ident = url + "?" + params_str
    return total_ident.upper() # Creating the identifier

def make_requests(endpoint_url, params_dict):
    global token_cache
    global data_cache
    global yelp_session
    ident = create_request_identifier(endpoint_url, params_dict)
    data_dict = data_cache.get_from_cache(ident)
    if data_dict:
        print("Loading from data cache: {}... data".format(ident))
    else:
        print("Fetching new data from {}".format(endpoint_url))
        token_dict = token_cache.get_from_cache('yelp')
        if not yelp_session:
            if token_dict:
                yelp_session = Session(token_dict)
            else:
                yelp_session = Session()
        data_dict = yelp_session.get_data_from_api(ident, endpoint_url, params_dict)
    return data_dict

