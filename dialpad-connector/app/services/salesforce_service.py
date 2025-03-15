import requests
from fastapi import HTTPException
from config import SALESFORCE_OAUTH_URL, CLIENT_ID, CLIENT_SECRET, USERNAME, PASSWORD
import redis

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



