from django.http import HttpResponse
import os
import sys
#import requests
#from rest_framework import status
#from pymongo import MongoClient
import json
from database.management import mongo_management as mm

DATABASE_NAME='database'
DATABASE_HOST='localhost'
DATABASE_PORT=27017
DATABASE_USER='user'
DATABASE_PASSWORD='pass'
REGIONS_COLLECTION ='test'


'''
dependencies needed on server: pymongo, environs
django forbids relative imports above top level
another relative imports problem: our pwd in docker will be changed to "/code"
'''
# print("Working Dir: ")
# print(os.getcwd())
'''
def database():
    MongoManagement client;
    client = MongoClient(host=DATABASE_HOST,
                            port=int(DATABASE_PORT),
                            username=DATABASE_USER,
                            password=DATABASE_PASSWORD
                            )
    userdb = client["user-db"]
    users = userdb["users"]
    print('ok')
    return users
'''
def edit_documents (request, document_id=None):
        mongoClient = mm.MongoManagement()
        id = document_id
        if request.method == 'POST':
            init_user = {"ID": 0,
                         "name": "admin",
                         "password": "admin",
                         "symmetricKey": "",
                         "privateKey-PSS": "",
                         "publicKey-PSS": "",
                         "privateKey-OAEP": "",
                         "publicKey-OAEP": "",
                         "encryptedFilePath": ""}
            mongoClient.add_user(init_user)
            return HttpResponse(id)
        elif request.method == 'GET':
            print("Are we there yet?")

            #if(id == 1):
            print("Jepsindda")
            for i in range(10):
                print(mongoClient.return_user(i))
            return HttpResponse(mongoClient.return_user(1))


# users/ & users/{id}
def create_user(request, document_id=None):
    mongoClient = mm.MongoManagement()
    id = document_id
    if request.method == 'GET':
        return HttpResponse(mongoClient.return_user(id))
    elif request.method == 'POST':
        data = request.body.decode('UTF-8')
        print(data)
        jsondata = json.loads(data)
        print("name: ")
        print(jsondata['name'])
        mongoClient.add_user(jsondata)
        return HttpResponse(1)
