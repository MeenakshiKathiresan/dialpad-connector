from dotenv import load_dotenv
import os

load_dotenv()

SALESFORCE_OAUTH_URL = os.getenv("SALESFORCE_OAUTH_URL")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
SECURITY_TOKEN = os.getenv("SECURITY_TOKEN")
