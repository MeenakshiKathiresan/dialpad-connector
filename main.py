from fastapi import FastAPI, HTTPException
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Salesforce credentials from environment variables
SALESFORCE_OAUTH_URL = os.getenv("SALESFORCE_OAUTH_URL")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
SECURITY_TOKEN = os.getenv("SECURITY_TOKEN")

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

        print("Error response:", response.json())
        raise HTTPException(status_code=400, detail="Failed")


@app.get("/list-objects")
async def list_salesforce_objects():
    """Fetch all Salesforce objects."""

    access_token, instance_url = get_salesforce_token()
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    url = f"{instance_url}/services/data/v58.0/sobjects/"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.json())


    
@app.post("/post-call-data")
async def post_call_data():
    access_token, instance_url = get_salesforce_token()
    print(access_token)
    
    salesforce_url = f"{instance_url}/services/data/v58.0/sobjects/Event"


    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    event_data = {
        "Subject": "Customer Support Call test 2",
        "ActivityDateTime": "2024-03-12",
        "DurationInMinutes": 35,
        "Description": "Transcription of the call."
    }

    response = requests.post(salesforce_url, json=event_data, headers=headers)

    if response.status_code == 201:
        return {"message": "Call data stored successfully!", "salesforce_id": response.json().get("id")}
    else:
        print("Error:", response.json())
        raise HTTPException(status_code=400, detail="Failed to create Event in Salesforce")
