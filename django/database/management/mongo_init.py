#!/usr/bin/env python3

# import the MongoClient class
from pymongo import MongoClient, errors

# global variables for MongoDB host (default port is 27017)
DOMAIN = 'localhost'
PORT = 27017

# use a try-except indentation to catch MongoClient() errors
try:
    # try to instantiate a client instance
    client = MongoClient(
        host = [ str(DOMAIN) + ":" + str(PORT) ],
        serverSelectionTimeoutMS = 3000, # 3 second timeout
        username = "user",
        password = "pass",
    )

    # print the version of MongoDB server if connection successful
    print("Connected!")
    print("server version:", client.server_info()["version"])


except errors.ServerSelectionTimeoutError as err:
    # set the client and DB name list to 'None' and `[]` if exception
    client = None

    # catch pymongo.errors.ServerSelectionTimeoutError
    print("pymongo ERROR:", err)


# Create user db
try:

    userdb = client["user-db"]
    users = userdb["users"]

    # Create admin-user
    if not users.find_one():

        init_user = {"ID": 0,
                     "name": "admin",
                     "password": "admin",   # ToDo: Change xD
                     "symmetricKey": "",
                     "privateKey-PSS": "",
                     "publicKey-PSS": "",
                     "privateKey-OAEP": "",
                     "publicKey-OAEP": "",
                     "encryptedFilePath": ""}

    x = users.insert_one(init_user)


except Exception as e:
    print(e)

print(client.list_database_names())

for x in users.find():
    print(x)
