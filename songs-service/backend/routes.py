from . import app
import os
import json
import pymongo
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401
from pymongo import MongoClient
from bson import json_util
from pymongo.errors import OperationFailure
from pymongo.results import InsertOneResult
from bson.objectid import ObjectId
import sys

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "songs.json")
songs_list: list = json.load(open(json_url))


# connect to database
db_client = MongoClient('localhost', 27017)

data = db_client.detals
# create a collection
storage = data.songs

# insert data
# status = storage.insert_many(songs_list)
# print(status)

# Delete all documents in the collection
# storage.delete_many({})

# Find all data 
# senso_data = storage.find()
# print(senso_data)
# for data in senso_data:
#     print(data)



def parse_json(data):
    return json.loads(json_util.dumps(data))


@app.route("/health")
def healthz():
    return jsonify(dict(status="OK")), 200

@app.route("/count")
def count():
    """return length of data"""
    count = storage.count_documents({})

    return {"count": count}, 200

@app.route("/song", methods=["GET"])
def songs():
    results = list(storage.find({}))
    print(results[0])
    return {"songs": parse_json(results)}, 200

@app.route("/song/<int:id>", methods=["GET"])
def get_song_by_id(id):
    song = storage.find_one({"id": id})
    if not song:
        return {"message": f"song with id {id} not found"}, 404
    return parse_json(song), 200

@app.route("/song", methods=["POST"])
def create_song():
    # get data from the json body
    song_in = request.json

    print(song_in["id"])

    # if the id is already there, return 303 with the URL for the resource
    song = storage.find_one({"id": song_in["id"]})
    if song:
        return {
            "Message": f"song with id {song_in['id']} already present"
        }, 302

    insert_id: InsertOneResult = storage.insert_one(song_in)

    return {"inserted id": parse_json(insert_id.inserted_id)}, 201

@app.route("/song/<int:id>", methods=["PUT"])
def update_song(id):

    # get data from the json body
    song_in = request.json

    song = storage.find_one({"id": id})

    if song == None:
        return {"message": "song not found"}, 404

    updated_data = {"$set": song_in}

    result = storage.update_one({"id": id}, updated_data)

    if result.modified_count == 0:
        return {"message": "song found, but nothing updated"}, 200
    else:
        return parse_json(storage.find_one({"id": id})), 201
    
@app.route("/song/<int:id>", methods=["DELETE"])
def delete_song(id):

    result = storage.delete_one({"id": id})
    if result.deleted_count == 0:
        return {"message": "song not found"}, 404
    else:
        return "", 204