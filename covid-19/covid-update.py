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
    
    'CA' : ['585-775-2876','559-285-1804','917-923-4245'],
    'FL' : ['614-648-4339'],
    'WA' : ['586-202-2795']
    }
    
    account_sid = "AC190283ede209f2f0abd10442d2758561"
    auth_token = "a04994bfa92f66684e47ba879f33a116"
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

