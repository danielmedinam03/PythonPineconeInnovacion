from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Configuración inicial
load_dotenv(".env")
uri = os.getenv("MONGO_URI")
client = MongoClient(uri)
db = client[os.getenv("MONGO_DATABASE")]
collection = db["feedback"]


def save_feedback(data):
    client = MongoClient(uri)
    collection.insert_one(data)
