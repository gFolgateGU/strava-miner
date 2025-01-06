import requests
import json
import os
import sys

from dotenv import load_dotenv

from services.activity_fetcher_service import ActivityFetcherService

# Load environment variables from .env file
load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REFRESH_TOKEN = os.getenv('REFRESH_TOKEN')
TOKEN_URL = os.getenv('TOKEN_URL')
ACTIVITIES_URL = os.getenv('ACTIVITIES_URL')

DB_SERVER = os.getenv('DB_SERVER')
DB_NAME = os.getenv('DB_NAME')
DB_PORT = os.getenv('DB_PORT')
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')

def get_access_token():
    # Declare globals
    global CLIENT_ID
    global CLIENT_SECRET
    global REFRESH_TOKEN
    global TOKEN_URL
    global ACTIVITIES_URL

    global DB_SERVER
    global DB_NAME
    global DB_PORT
    global DB_USERNAME
    global DB_PASSWORD

    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'refresh_token',
        'refresh_token': REFRESH_TOKEN
    }
    print(TOKEN_URL)
    response = requests.post(TOKEN_URL, data=data)
    response_data = response.json()

    if response.status_code != 200:
        print(f"Failed to get access token: {response.status_code}")
        return None
    
    new_refresh_token = response_data.get('refresh_token')
    if new_refresh_token:
        os.environ['REFRESH_TOKEN'] = new_refresh_token
        with open('.env', 'w') as file:
            file.write(f'CLIENT_ID={CLIENT_ID}\n')
            file.write(f'CLIENT_SECRET={CLIENT_SECRET}\n')
            file.write(f'REFRESH_TOKEN={new_refresh_token}\n')
            file.write(f'TOKEN_URL={TOKEN_URL}\n')
            file.write(f'ACTIVITIES_URL={ACTIVITIES_URL}\n')
            file.write(f'DB_SERVER={DB_SERVER}\n')
            file.write(f'DB_NAME={DB_NAME}\n')
            file.write(f'DB_PORT={DB_PORT}\n')
            file.write(f'DB_USERNAME={DB_USERNAME}\n')
            file.write(f'DB_PASSWORD={DB_PASSWORD}\n')
    
    return response_data.get('access_token')

def main():
    # Attempt to get an access token to get updated strava data
    access_token = get_access_token()
    if access_token is None:
        return
    
    act_fetcher = ActivityFetcherService(access_token, ACTIVITIES_URL)
    act_fetcher.get_activities()
    
if __name__ == "__main__":
    main()
