import requests
import json
from os import getenv
from dotenv import load_dotenv

load_dotenv()
    username = getenv('username')
    password = getenv('password')

headers = {
    'Content-type':'application/json',
    'Accept':'application/json',
    'X-ESA-API-Key':'ROBOT'
}

def login(username, password):
    session = requests.Session()
    login_request = {"type":"STANDARD_LOGIN", "login":username, "password":password}
    request = session.post('https://www.veikkaus.fi/api/bff/v1/sessions', data=json.dumps(login_request), headers=headers)
    if request.status_code == 200:
        return session
    else:
        raise Exception("Authentication failed", request.status_code)

def main():
    session = login(username, password)
    result = session.get('https://www.veikkaus.fi/api/toto-info/v1/cards/active')
    result_json_data = json.loads(result.text)
    print("Tämänpäiväinen ja tulevat toto-kohteet")
    print("==========================================")
    for entry in result_json_data['collection']:
        print(entry)
        print("\n\n")

main()