import requests
import json
from datetime import datetime
from sqlalchemy.dialects.postgresql import insert

from models.models import Activity


class ActivityFetcherService:
    def __init__(self, access_token, activites_url, db_session):
        self.access_token = access_token
        self.activites_url = activites_url
        self.db_session = db_session
        self.headers = {
            'Authorization': f'Bearer {self.access_token}'
        }


    def get_activities(self):
        start_date = datetime(2024, 9, 1, 0, 0, 0).timestamp()
        end_date = datetime(2024, 10, 1, 0, 0, 0).timestamp()

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

    def upsert_activity(self, activity):
        session = None
        try:
            # Start a new session
            session = self.db_session()

            stmt = insert(Activity).values(
                activity_id=activity.activity_id,
                strava_id=activity.strava_id,
                name=activity.name,
                distance=activity.distance,
                moving_time=activity.moving_time,
                elapsed_time=activity.elapsed_time,
                total_elevation_gain=activity.total_elevation_gain,
                type=activity.type,
                start_date=activity.start_date,
                start_date_local=activity.start_date_local,
                average_speed=activity.average_speed,
                max_speed=activity.max_speed,
                average_cadence=activity.average_cadence,
                average_heartrate=activity.average_heartrate,
                max_heartrate=activity.max_heartrate
            )
            stmt = stmt.on_conflict_do_update(
                index_elements=['activity_id'],
                set_={ 
                    'strava_id': stmt.excluded.strava_id,
                    'name': stmt.excluded.name,
                    'distance': stmt.excluded.distance,
                    'moving_time': stmt.excluded.moving_time,
                    'elapsed_time': stmt.excluded.elapsed_time,
                    'total_elevation_gain': stmt.excluded.total_elevation_gain,
                    'type': stmt.excluded.type,
                    'start_date': stmt.excluded.start_date,
                    'start_date_local': stmt.excluded.start_date_local,
                    'average_speed': stmt.excluded.average_speed,
                    'max_speed': stmt.excluded.max_speed,
                    'average_cadence': stmt.excluded.average_cadence,
                    'average_heartrate': stmt.excluded.average_heartrate,
                    'max_heartrate': stmt.excluded.max_heartrate
                }
            )
            # Execute the statement
            session.execute(stmt)     
            # Commit the transaction
            session.commit()
        except Exception as error:
            # Roll back the transaction in case of an error
            if session:
                session.rollback()
            print(f"Error: {error}")
        finally:
            # Close the session
            if session:
                session.close()        
    
    def upsert_activities(self, activities):
        for activity in activities:
            self.upsert_activity(activity)
