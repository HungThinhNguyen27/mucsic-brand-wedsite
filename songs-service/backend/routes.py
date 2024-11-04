from . import app
import os
import json
import pymongo
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401
from pymongo import MongoClient
from bson import json_util
from pymongo.errors import ConnectionFailure, OperationFailure
from pymongo.results import InsertOneResult
from bson.objectid import ObjectId
import sys

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "songs.json")
songs_list: list = json.load(open(json_url))


def connect_mongo():
    try:
        # connect to database NoSQL
        client = MongoClient(
            host='mongodb',
            port=27017,
            username='thinh',
            password='thinh123',
            authSource="admin"
        )
        db_client = client["test-connection"]
        print("Connected to MongoDB successfully!")
        songs_collection = db_client["songs"]
        print("Create Songs Collection successfully!")

        return db_client, songs_collection

    except ConnectionFailure as e:
        print(f"Could not connect to MongoDB: {e}")
        return None

    except OperationFailure as e:
        print(f"Authentication failed: {e}")
        return None

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
    
db_client, songs_collection = connect_mongo()

# Delete all documents in the collection
# storage.delete_many({})

# Find all data 
# senso_data = storage.find()
# print(senso_data)
# for data in senso_data:
#     print(data)



@app.route("/")
def insert():
    songs_collection.insert_many(songs_list)
    return jsonify(dict(status="OK")), 200


def parse_json(data):
    return json.loads(json_util.dumps(data))

@app.route("/health")
def healthz():
    return jsonify(dict(status="OK")), 200

@app.route("/count")
def count():
    """return length of data"""
    count = songs_collection.count_documents({})

    return {"count": count}, 200

@app.route("/song", methods=["GET"])
def songs():
    results = list(songs_collection.find({}))
    print(results[0])
    return {"songs": parse_json(results)}, 200

@app.route("/song/<int:id>", methods=["GET"])
def get_song_by_id(id):
    song = songs_collection.find_one({"id": id})
    if not song:
        return {"message": f"song with id {id} not found"}, 404
    return parse_json(song), 200

@app.route("/song", methods=["POST"])
def create_song():
    # get data from the json body
    song_in = request.json

    print(song_in["id"])

    # if the id is already there, return 303 with the URL for the resource
    song = songs_collection.find_one({"id": song_in["id"]})
    if song:
        return {
            "Message": f"song with id {song_in['id']} already present"
        }, 302

    insert_id: InsertOneResult = songs_collection.insert_one(song_in)

    return {"inserted id": parse_json(insert_id.inserted_id)}, 201

@app.route("/song/<int:id>", methods=["PUT"])
def update_song(id):

    # get data from the json body
    song_in = request.json

    song = songs_collection.find_one({"id": id})

    if song == None:
        return {"message": "song not found"}, 404

    updated_data = {"$set": song_in}

    result = songs_collection.update_one({"id": id}, updated_data)

    if result.modified_count == 0:
        return {"message": "song found, but nothing updated"}, 200
    else:
        return parse_json(songs_collection.find_one({"id": id})), 201
    
@app.route("/song/<int:id>", methods=["DELETE"])
def delete_song(id):

    result = songs_collection.delete_one({"id": id})
    if result.deleted_count == 0:
        return {"message": "song not found"}, 404
    else:
        return "", 204
    

# docker network connect app-network songs-service-flask_app-1

