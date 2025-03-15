from fastapi import APIRouter
from services.salesforce_service import post_call_data_to_salesforce
from services.dial_pad_service import get_dialpad_calls
from models.Call import Call
import requests

router = APIRouter()

@router.post("/post-call")
async def post_call_data():
    call_list: list[Call] = get_dialpad_calls()
    return post_call_data_to_salesforce(call_list)
    