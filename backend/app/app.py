# app/app.py
from flask import Flask, jsonify, request, abort
from pymongo import MongoClient
from pymongo.collection import Collection
import os

# local files
from backend.app.routes.pwd import getAllpwd, postpwd, getOnepwd, updatepwd, deletepwd, testPost
from backend.app.routes.acct import getAllacct, patchacct, deleteacct, init

# TODO: add login
# TODO: add logging
# TODO: add rate limit
# TODO: frontend


app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello, Dockerized Flask with MongoDB!"


@app.route('/data/pwd', methods=['GET', 'POST'])
@app.route('/data/pwd/<index>', methods=['GET', 'PATCH', 'DELETE'])
def pwd(index=None):
    if index is None:
        if request.method == "GET":
            db = connect("passwords")
            rtn = getAllpwd(db)
            return jsonify(rtn)
        elif request.method == "POST":
            # add to data
            pwdDb = connect("passwords")
            acctDb = connect("accountTypes")
            # testPost(pwdDb, acctDb)
            rtn = postpwd(pwdDb, acctDb, request.get_json())
            if rtn is not None:
                abort(422, rtn)
            return 'POSTED'
        else:
            abort(405)
    elif index is not None:
        if request.method == "GET":
            pwdDb = connect("passwords")
            rtn = getOnepwd(pwdDb, index)
            return jsonify(rtn)
        elif request.method == "PATCH":
            # update that data
            pwdDb = connect("passwords")
            rtn = updatepwd(pwdDb, request.get_json())
            return rtn
        elif request.method == "DELETE":
            # soft delete that item
            pwdDb = connect("passwords")
            rtn = deletepwd(pwdDb, index)
            return rtn
        else:
            abort(405)
    else:
        abort(405)


@app.route('/data/acct', methods=['GET', 'POST'])
@app.route('/data/acct/<index>', methods=['DELETE'])
def acct(index=None):
    if index is None:
        if request.method == "GET":
            acctDb = connect("accountTypes")
            rtn = getAllacct(acctDb)
            return jsonify(rtn)
        elif request.method == "POST":
            acctDb = connect("accountTypes")
            rtn = patchacct(acctDb, request.get_json())
            return jsonify(rtn)
            # init(acctDb)
        else:
            abort(405)
    else:
        if request.method == "DELETE":
            acctDb = connect("accountTypes")
            rtn = deleteacct(acctDb, index)
            return jsonify(rtn)
        else:
            abort(405)


def connect(database: str) -> Collection:
    # MongoDB connection using environment variables
    client = MongoClient(os.getenv("MONGO_URI", "mongodb://mongo:27017/"))
    db = client["isidore"]
    return db[database]


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
