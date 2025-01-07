import requests
import json
from datetime import datetime

from models.models import Activity

class ActivityFetcherService:
    def __init__(self, access_token, activites_url):
        self.access_token = access_token
        self.activites_url = activites_url
        self.headers = {
            'Authorization': f'Bearer {self.access_token}'
        }


    def get_activities(self):
        start_date = datetime(2024, 12, 1, 0, 0, 0).timestamp()
        end_date = datetime(2025, 1, 1, 0, 0, 0).timestamp()

        params = {
            'after': int(start_date),
            'before': int(end_date)
        }

        try:
            response = requests.get(self.activites_url, headers=self.headers, params=params)
            if response.status_code != 200:
                print(f"Error response: {response.json()}")
                raise Exception(f"Failed to fetch activities: {response.status_code} - {response.text}")
                return None
            activities_json = response.json()
            activities = []
            for activity_json in response.json():
                activity = Activity(activity_id=activity_json["id"],
                                    strava_id=activity_json["athlete"]["id"],
                                    name=activity_json.get("name", "Unknown"),
                                    distance=activity_json.get("distance", 0.0),
                                    moving_time=activity_json.get("moving_time", 0),
                                    elapsed_time=activity_json.get("elapsed_time", 0),
                                    total_elevation_gain=activity_json.get("total_elevation_gain", 0.0),
                                    type=activity_json.get("type", "Unknown"),
                                    start_date=activity_json.get("start_date"),
                                    start_date_local=activity_json.get("start_date_local"),
                                    average_speed=activity_json.get("average_speed", 0.0),
                                    max_speed=activity_json.get("max_speed", 0.0),
                                    average_cadence=activity_json.get("average_cadence", 0.0),
                                    average_heartrate=activity_json.get("average_heartrate", 0.0),
                                    max_heartrate=activity_json.get("max_heartrate", 0.0))
                activities.append(activity)
            return activities
        except Exception as e:
            print(e)
            return None

    def upsert_activities(self, activities):
        print(f'I got {len(activities)} activities to upsert')
