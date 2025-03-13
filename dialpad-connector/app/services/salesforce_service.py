import requests
from fastapi import HTTPException
from config import SALESFORCE_OAUTH_URL, CLIENT_ID, CLIENT_SECRET, USERNAME, PASSWORD

def get_salesforce_token():
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
        return access_token, instance_url
    else:
        raise HTTPException(status_code=400, detail="Failed to authenticate with Salesforce")
