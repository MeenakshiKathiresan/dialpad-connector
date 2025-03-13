from fastapi import APIRouter, HTTPException
from services.salesforce_service import get_salesforce_token
import requests

router = APIRouter()

@router.post("/post-call")
async def post_call_data():
    access_token, instance_url = get_salesforce_token()
    salesforce_url = f"{instance_url}/services/data/v58.0/sobjects/Event"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

    event_data = {
        "Subject": "Customer Support Call test 4",
        "ActivityDateTime": "2024-03-12",
        "DurationInMinutes": 5,
        "Description": "Transcription"
    }

    response = requests.post(salesforce_url, json=event_data, headers=headers)

    if response.status_code == 201:
        return {"message": "Call data stored successfully!", "salesforce_id": response.json().get("id")}
    else:
        raise HTTPException(status_code=400, detail="Failed to create Event in Salesforce")
