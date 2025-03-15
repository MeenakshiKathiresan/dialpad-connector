from fastapi import APIRouter, HTTPException
from services.salesforce_service import get_salesforce_token
from services.dial_pad_service import get_dialpad_calls
from models.Call import Call
import requests

router = APIRouter()

@router.post("/post-call")
async def post_call_data():
    
    call_list: list[Call] = get_dialpad_calls()

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