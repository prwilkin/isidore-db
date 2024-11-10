from dotenv import load_dotenv
from datetime import datetime
from pymongo.collection import Collection
from bson import ObjectId
import os, pytz

# local files
from backend.app.encrypt import decrypt_data, encrypt_data


def insertpwd(db: Collection, data):
    schema = {"site": None, "account_type": None, "user_name": None, "email": None, "password": None,
              "security_qs": None, "phone": None, "created_at": None, "updated_at": None, "deleted_at": None}
    for i in data.keys():
        schema[i] = data[i]
    db.insert_one(schema)


def validate_acct(db: Collection, data: str) -> bool:
    accounts = []
    for x in db.find({"deletedAt": None}, {"_id": 0}):
        accounts.append(x['site'])
    if data not in accounts:
        return False
    else:
        return True


def validate_user(user: str, email: str) -> bool:
    if user is None or email is None:
        return False
    else:
        return True


def validate_pass(password: str):
    if password is None:
        return False
    else:
        encrypted_data, iv, salt = encrypt_data(password)
        return {"encrypted_data": encrypted_data, "iv": iv, "salt": salt}


def validate_secQ(data: dict):
    for x in range(len(data)):
        if data[x]['q'] is None or data[x]['a'] is None:
            return False
        encrypted_data, iv, salt = encrypt_data(data[x]['a'])
        data[x]['a'] = {"encrypted_data": encrypted_data, "iv": iv, "salt": salt}
    return data


def getAllpwd(db: Collection) -> list:
    data = db.find({"deletedAt": None}, {"deleted_At": 0, "created_at": 0, "updated_At": 0})
    rtn = []
    # clean up data
    for row in data:
        load_dotenv()
        password = os.getenv("ENCRYPTION_PASSWORD")

        row["_id"] = str(row["_id"])

        # decrypt password
        if row.get("password") is not None:
            row["password"] = decrypt_data(row["password"]["encrypted_data"], row["password"]["iv"], row["password"]["salt"])
        # decrypt answer
        if row.get("security_qs") is not None:
            for x in range(len(row["security_qs"])):
                data = row["security_qs"][x]['a']
                row["security_qs"][x]['a'] = decrypt_data(data["encrypted_data"], data["iv"], data["salt"])
        rtn.append(row)
    return rtn


def postpwd(pwdDb: Collection, acctDb: Collection, data: dict):
    # validate account type
    valid = validate_acct(acctDb, data["account_type"])
    if valid is False:
        return 'Invalid account type'

    # get time
    created = datetime.now(pytz.timezone('America/New_York'))

    # continue validation and posting
    if data["account_type"] == "Same Site":
        valid = validate_user(data["user_name"], data["email"])
        if valid is False:
            return 'Username or Email is missing'
        valid = validate_pass(data["password"])
        if valid is False:
            return 'Password is missing'
        else:
            data["password"] = valid

        # we have account_type, user/email, and password at this point enough to post

        if data.get("security_qs") is not None:
            # validate sec q's and encrypt
            valid = validate_secQ(data["security_qs"])
            if valid is False:
                return 'Security Question or Answer missing'
            else:
                data["security_qs"] = valid
            # post with questions
            insertpwd(pwdDb, {"site": data["site"], "account_type": data["account_type"], "user_name": data["user_name"],
                              "email": data["email"], "password": data["password"], "security_qs": data["security_qs"],
                              "phone": data["phone"], "created_at": created})
        # no q's
        else:
            insertpwd(pwdDb, {"site": data["site"], "account_type": data["account_type"],
                              "user_name": data["user_name"], "email": data["email"], "password": data["password"],
                              "phone": data["phone"], "created_at": created})
    # post this
    else:
        insertpwd(pwdDb, {"site": data["site"], "account_type": data["account_type"], "created_at": created})
    return None


def getOnepwd(pwdDb: Collection, index):
    index = ObjectId(index)
    data = pwdDb.find_one({"_id": index}, {"deleted_At": 0, "created_at": 0, "updated_At": 0})
    load_dotenv()
    password = os.getenv("ENCRYPTION_PASSWORD")

    data["_id"] = str(data["_id"])

    # decrypt password
    if data.get("password") is not None:
        data["password"] = decrypt_data(data["password"]["encrypted_data"], data["password"]["iv"], data["password"]["salt"])
    # decrypt answer
    if data.get("security_qs") is not None:
        for x in range(len(data["security_qs"])):
            y = data["security_qs"][x]['a']
            data["security_qs"][x]['a'] = decrypt_data(y["encrypted_data"], y["iv"], y["salt"])
    return data


def updatepwd(pwdDb: Collection, data: dict):
    valid = validate_user(data["user_name"], data["email"])
    if valid is False:
        return 'Username or Email is missing'

    valid = validate_pass(data["password"])
    if valid is False:
        return 'Password is missing'
    else:
        data["password"] = valid

    # get time
    updated = datetime.now(pytz.timezone('America/New_York'))
    data.update({"updated_at": updated})

    if data.get("security_qs") is not None:
        valid = validate_secQ(data["security_qs"])
        if valid is False:
            return 'Security Question or Answer missing'
        else:
            data["security_qs"] = valid
    objId = ObjectId(data["_id"])
    data.pop("_id")
    pwdDb.update_one({"_id": objId}, {"$set": data})
    return "UPDATED"


def deletepwd(pwdDb: Collection, index):
    index = ObjectId(index)
    deleted = datetime.now(pytz.timezone('America/New_York'))
    pwdDb.update_one({"_id": index}, {"$set": {"deleted_At": deleted}})
    return "DELETED"


def testPost(pwdDb: Collection, acctDb: Collection):
    # pwdDb.insert_one({"site": None, "account_type": None, "user_name": None, "email": None, "password": None,
    #                   "security_qs": None, "phone": None, "created_at": None, "updated_at": None, "deleted_at": None})
    acctDb.insert_many([{"site": "Google", "deleted_at": None}, {"site": "Facebook", "deleted_at": None},
                        {"site": "Twitter", "deleted_at": None}, {"site": "GitHub", "deleted_at": None},
                        {"site": "Same Site", "deleted_at": None}])
    # x = acctDb.find({}, {"_id": 0})
    # for x in x:
    #     print(x)
    return



