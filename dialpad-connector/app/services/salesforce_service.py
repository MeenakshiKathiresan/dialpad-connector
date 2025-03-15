import requests
from fastapi import HTTPException
from config import SALESFORCE_OAUTH_URL, CLIENT_ID, CLIENT_SECRET, USERNAME, PASSWORD
import redis
from models.Call import Call

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
ACCESS_TOKEN_KEY = "salesforce_access_token"
INSTANCE_URL_KEY = "salesforce_instance_url"

def get_salesforce_token():
    access_token = redis_client.get(ACCESS_TOKEN_KEY)
    instance_url = redis_client.get(INSTANCE_URL_KEY)
    
    if access_token and instance_url:
        return access_token, instance_url

    payload = {
        'grant_type': 'password',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'username': USERNAME,
        'password': PASSWORD 
    }
    response = requests.post(SALESFORCE_OAUTH_URL, data=payload)
    
    if response.status_code == 200:
        access_token = response.json().get('access_token')
        instance_url = response.json().get('instance_url') 
        redis_client.set(ACCESS_TOKEN_KEY, access_token)
        redis_client.set(INSTANCE_URL_KEY, instance_url)
        return access_token, instance_url
    else:
        raise HTTPException(status_code=400, detail="Failed to authenticate with Salesforce")

def post_call_data_to_salesforce(call_list: list[Call]):
    access_token, instance_url = get_salesforce_token()
    salesforce_url = f"{instance_url}/services/data/v58.0/sobjects/Event"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

    results = {
        "successful": [],
        "failed": []
    }

    for call in call_list:
        event_data = {
            "Subject": f"{call.subject} to {call.phone}",  
            "ActivityDateTime": call.activity_date.isoformat(), 
            "DurationInMinutes": call.duration_in_minutes,
            "Description": call.phone,  
        }
        response = requests.post(salesforce_url, json=event_data, headers=headers)

        if response.status_code == 201:
            results["successful"].append(response.json().get("id"))
        else:
            results["failed"].append(response.text)
        
    return {
        "message": f"{len(results)} calls posting completed.",
        "results": results
    }
    
