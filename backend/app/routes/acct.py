from pymongo.collection import Collection
from datetime import datetime
from bson import ObjectId
import pytz


def getAllacct(db: Collection):
    rtn = []
    for x in db.find({"deleted_at": None}):
        x["_id"] = str(x["_id"])
        rtn.append(x)
    return rtn


def patchacct(db: Collection, data):
    db.insert_one({"site": data["site"], "deleted_at": None})
    return getAllacct(db)


def deleteacct(db: Collection, index):
    deleted = datetime.now(pytz.timezone('America/New_York'))
    db.update_one({"_id": ObjectId(index)}, {"$set": {"deleted_at": deleted}})
    return getAllacct(db)


def init(db: Collection):
    db.insert_many([{"site": "Google", "deleted_at": None}, {"site": "Facebook", "deleted_at": None},
                        {"site": "Twitter", "deleted_at": None}, {"site": "GitHub", "deleted_at": None},
                        {"site": "Same Site", "deleted_at": None}])
