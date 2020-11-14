#!/usr/bin/env python3

# import the MongoClient class
from pymongo import MongoClient, errors


class MongoManagement:

    def __init__(self):

        self.db_name = "database"
        self.db_host = "localhost"
        self.db_port = 27017
        self.db_user = "user"
        self.db_password = "pass"

        # ToDo: Replace with .env variables!

        self.client = MongoClient(
            host = [ self.db_host + ":" + str(self.db_port) ],
            serverSelectionTimeoutMS = 3000, # 3 second timeout
            username = self.db_user,
            password = self.db_password,
        )
        print("Connected!")
        self.userdb = self.client["user-db"]
        self.users = self.userdb["users"]

    def add_user(self, user):
        """
        Insert new user into user-db
        :param user: user data dictionary
        :return:
        """

        _id = self.users.insert_one(user)

        return _id

    def delete_user(self, user_id):
        """
        Delete user with ID = user_id
        :param user_id: ID
        :return:
        """
        self.users.delete_one({"ID": user_id})

    def update_user(self, user_id, attribute):
        """
        Update attribute from user ID
        :param user_id: ID
        :param attribute: attribute dictionary
        :return:
        """
        pass

    def return_user(self, user_id):
        """
        Returns user credentials
        :param user_id: ID
        :return: database entry of user with ID = user_id
        """
        return self.users.find_one({"ID": user_id})

    def delete_all_users(self):
        """
        Deletes all user entries in user-db
        :return:
        """
        x = self.users.delete_many({})


if __name__ == "__main__":

    from random import randint

    man = MongoManagement()
    user_id = randint(1, 10000000000000)
    new_user = {"ID": user_id,
                "name": "init",
                "password": "kjldasfhklasdjfh",
                "symmetricKey": "dfdfdfdf",
                "privateKey-PSS": "dfdsfadsfa",
                "publicKey-PSS": "adsfasdf",
                "privateKey-OAEP": "asdfasdfasdf",
                "publicKey-OAEP": "asdfadsfas",
                "encryptedFilePath": "/test/test/test"
                }
    _id = man.add_user(new_user)
    print("_id: " + str(_id))
    user = man.return_user(user_id)
    print(user)
    man.delete_user(user_id)
    user = man.return_user(user_id)
    print(user)
