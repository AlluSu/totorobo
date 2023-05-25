import requests
import json
from os import getenv
from dotenv import load_dotenv
from datetime import date

load_dotenv()
username = getenv('username')
password = getenv('password')

BASE_URL_CARDS = 'https://www.veikkaus.fi/api/toto-info/v1/cards/'

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

def print_request_data(data, event_text):
    print("\n ========================================== \n")
    for entry in data['collection']:
        print(entry)
        print("\n")

def get_data(session, url):
    result = session.get(url)
    json_data = json.loads(result.text)
    return json_data

def main():
    session = login(username, password)
    event = int(input("Anna tapahtuma: \n 1. Tänään \n 2. Tulevat \n 3. Kuluvan päivän & tulevat \n 4. Tietty päivä muodossa YYYY-MM-DD \n : "))
    if (event == 1):
        url = BASE_URL_CARDS + 'today'
        response = get_data(session, url)
        event_text = "Tämänpäiväiset toto-kohteet"
        print_request_data(response, event_text)

    elif (event == 2):
        url = BASE_URL_CARDS + 'future'
        response = get_data(session, url)
        event_text = "Tulevat toto-kohteet"
        print_request_data(response, event_text)

    elif (event == 3):
        url = BASE_URL_CARDS + 'active'
        response = get_data(session, url)
        event_text = "Kuluvan päivän & tulevat toto-kohteet"
        print_request_data(response, event_text)

    elif (event == 4):
        date = input("Anna päivämäärä muodossa YYY-MM-DD: ")
        url = BASE_URL_CARDS + 'date/' + str(date)
        response = get_data(session, url)
        event_text = "Toto-kohteet " + str(date)
        print_request_data(response, event_text)

    else:
        raise Exception("Invalid input")

main()