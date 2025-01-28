import requests
from secret import *
import requests

CLIENT_ID = '7f582119-f04a-4bcb-95c1-b0e050734109'
CLIENT_SECRET = get_secret()
GRANT_TYPE = 'client_credentials'
# LOCAL_DIR = './images'
SCOPE = 'https://graph.microsoft.com/.default'
TENANT_ID = '7a38fe56-35ab-4f3c-9e89-04fe0a0074d3'


def get_access_token():
    token_request_uri = "https://login.microsoftonline.com/{}/oauth2/v2.0/token".format(TENANT_ID)
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': GRANT_TYPE,
        'scope': SCOPE
    }
    resp = requests.post(
        token_request_uri,
        data=data,
    )
    token_response = resp.json()
    access_token = token_response.get('access_token')
    print("Access token retrieved")
    print(access_token)
    return access_token


#token = get_access_token()
