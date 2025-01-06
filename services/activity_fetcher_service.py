import requests
from datetime import datetime

class ActivityFetcherService:
    def __init__(self, access_token, activites_url):
        self.access_token = access_token
        self.activites_url = activites_url
    
    def get_activities(self):
        start_date = datetime(2024, 12, 1, 0, 0, 0).timestamp()
        end_date = datetime(2025, 1, 1, 0, 0, 0).timestamp()

        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        params = {
            'after': int(start_date),
            'before': int(end_date)
        }

        try:
            response = requests.get(self.activites_url, headers=headers, params=params)
            print(response.json())
            if response.status_code != 200:
                print(f"Error response: {response.json()}")
                raise Exception(f"Failed to fetch activities: {response.status_code} - {response.text}")
                return response.json()
        except Exception as e:
            print('e')
            return None
