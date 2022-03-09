from pymongo import MongoClient

client = MongoClient("localhost", 27017)

db = client.telebotdb
tele_bot_db = db.users


class DataBaseManagerUser:

    @classmethod
    def insert_user_data(cls, user_id: str, phone: str):
        data = {"phone": phone, "user_id": user_id}
        tele_bot_db.insert_one(data)
        return True

    @classmethod
    def check_login(cls, user_id):
        data = tele_bot_db.find_one({"user_id": user_id})
        if data is not None:
            return True
        else:
            return False

    @classmethod
    def users_list(cls):
        users_list = []
        users = tele_bot_db.find({})
        for user in users:
            users_list.append(user)
        return users_list
