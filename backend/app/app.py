# app/app.py
from flask import Flask, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

# MongoDB connection using environment variables
client = MongoClient(os.getenv("MONGO_URI", "mongodb://mongo:27017/"))
db = client["testdb"]
collection = db["testcollection"]

@app.route('/')
def hello():
    return "Hello, Dockerized Flask with MongoDB!"

@app.route('/data')
def get_data():
    # Insert a document to test the connection
    collection.insert_one({"name": "sample data"})
    data = list(collection.find({}, {"_id": 0}))
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
