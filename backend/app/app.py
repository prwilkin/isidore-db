# app/app.py
from flask import Flask, jsonify, request, abort
from pymongo import MongoClient
import os

# local files


app = Flask(__name__)

# MongoDB connection using environment variables
client = MongoClient(os.getenv("MONGO_URI", "mongodb://mongo:27017/"))
db = client["testdb"]
collection = db["testcollection"]


@app.route('/')
def hello():
    return "Hello, Dockerized Flask with MongoDB!"


@app.route('/data', methods=['GET', 'POST'])
@app.route('/data/<index>', methods=['GET', 'PATCH', 'DELETE'])
def data(index=None):
    if index is None:
        if request.method == "GET":
            # return all data
            return
        elif request.method == "POST":
            # add to data
            return
        else:
            abort(405)
    elif index is not None:
        if request.method == "GET":
            # return just that data
            return
        elif request.method == "PATCH":
            # update that data
            return
        elif request.method == "DELETE":
            # soft delete that item
            return
        else:
            abort(405)
    else:
        abort(405)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
