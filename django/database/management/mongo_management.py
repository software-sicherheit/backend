#!/usr/bin/env python3

# import the MongoClient class
from pymongo import MongoClient, errors
from environs import Env


class MongoManagement:

    def __init__(self):

        # Read from .env
        env = Env()
        env.read_env()

        self.db_name = str(env("DATABASE_NAME"))
        self.db_host = str(env("DATABASE_HOST"))
        self.db_port = int(env("DATABASE_PORT"))
        self.db_user = str(env("DATABASE_USER"))
        self.db_pass = str(env("DATABASE_PASSWORD"))

        try:
            self.client = MongoClient(
                host = [ str(self.db_host) + ":" + str(self.db_port) ],
                serverSelectionTimeoutMS = 3000, # 3 second timeout
                username = self.db_user,
                password = self.db_pass,
            )
            print("Connected!")
            self.userdb = self.client["user-db"]
            self.users = self.userdb["users"]

        except Exception as e:
            raise e

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

