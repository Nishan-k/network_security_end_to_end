from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

monog_uri = os.getenv("MONGO_DB_URL")

if not monog_uri:
    print("MONGO_DB_URL not found in in the .env file")
    exit()


client = MongoClient(monog_uri)

try:
    client.admin.command('ping')
    print("Connection is SUCCESSFULL.")
except Exception as e:
    print(f"Connection faile.{e}")

