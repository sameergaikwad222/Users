from pymongo.mongo_client import MongoClient
import json


def load_config(file_path):
    with open(file_path, "r") as f:
        config = json.load(f)
    return config


# Example usage
config = load_config("app/config/config.json")


uri = config["database"]["uri"]
dbname = config["database"]["database_name"]
collectionName = config["database"]["collection_name"]

try:
    client = MongoClient(host=uri)
    db = client.get_database(dbname)
    collection = db.get_collection(name=collectionName)
except Exception as e:
    print("database error : ", e)
    exit(1)
