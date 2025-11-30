from flask_pymongo import PyMongo
from bson.objectid import ObjectId

mongo = PyMongo()

def init_db(app):
    mongo.init_app(app)

def get_db():
    return mongo.db

def json_encoder(data):
    if isinstance(data, list):
        for item in data:
            if '_id' in item:
                item['_id'] = str(item['_id'])
    elif isinstance(data, dict):
        if '_id' in data:
            data['_id'] = str(data['_id'])
    return data
