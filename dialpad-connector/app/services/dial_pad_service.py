import requests
from fastapi import HTTPException
from config import DIALPAD_API_KEY
from models.Call import Call
import datetime

DIALPAD_BASE_URL = "https://dialpad.com/api/v2"  

# private helper functions
def _get_time(time_in_ms):
    timestamp_s = int(time_in_ms) / 1000
    return datetime.datetime.fromtimestamp(timestamp_s)

def _get_formatted_phone(phone):
    if len(phone) > 10:
        phone = f"{phone[:-10]}({phone[-10:-7]}) {phone[-7:-4]}-{phone[-4:]}"
    return phone
    
def _get_headers():
    headers = {
        "Authorization": f"Bearer {DIALPAD_API_KEY}",
        "Content-Type": "application/json",
    }
    return headers

def get_dialpad_calls():
    url = f"{DIALPAD_BASE_URL}/call"  
    response = requests.get(url, headers=_get_headers())

    if response.status_code == 200:
        call_list = []
        data = response.json()
        for call_data in data["items"]:
            call_id = call_data["call_id"]
            phone = _get_formatted_phone(call_data["contact"]["phone"])
            subject = call_data["direction"]
            duration_in_minutes = call_data["duration"]
            activity_date = _get_time(call_data["date_started"])
            call = Call(call_id, subject, activity_date, phone, duration_in_minutes)

            call_list.append(call)
        return call_list
    else:
        raise HTTPException(status_code=400, detail="Failed to authenticate with Dialpad")
