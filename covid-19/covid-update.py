import json
import requests
from requests.exceptions import HTTPError
from twilio.rest import Client


def state_info(state_lst = []):

    daily_url = 'https://covidtracking.com/api/states'
    print(state_lst)
    content = {}
    try:
        response = requests.get(daily_url)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        print('Success!')

    json_response = response.text
    print(type(json_response))
    data = json.loads(json_response)
    #print(data)
    for state in state_lst:
        for info in data:
            if info['state'] == state:
                content[state] = info
    return content

def msg_body(**content):

    print(content)
    phone_map = {
    
    'CA' : ['585-7XX-2XX6','5XCC-2XC5-XX04','9C7-9CR-4D45'],
    'FL' : ['6X4-64X-4XXX'],
    'WA' : ['5XX-XX2-2795']
    }
    
    account_sid = "AXXXXXXXXXXXX"
    auth_token = "aXXXXXXX"
    client = Client(account_sid, auth_token)

    for state in phone_map:
        for j in range(len(phone_map[state])):
            message = client.messages \
                        .create (
                            body = str(content[state]),
                            from_="+12057723413",
                            to=str(phone_map[state][j])
                        )
    
    print(message.sid)

if __name__ == "__main__":
    states = ['CA','FL','WA']
    content = state_info(states)
    msg_body(**content)

