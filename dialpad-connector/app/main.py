from fastapi import FastAPI
from api import  events

app = FastAPI()

app.include_router(events.router, prefix="/events", tags=["Events"])
