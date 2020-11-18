from django.http import HttpResponse
import os
import sys
import requests
from rest_framework import status
from pymongo import MongoClient

DATABASE_NAME='database'
DATABASE_HOST='localhost'
DATABASE_PORT=27017
DATABASE_USER='user'
DATABASE_PASSWORD='pass'
REGIONS_COLLECTION ='test'

def database():
    client = MongoClient(host=DATABASE_HOST,
                            port=int(DATABASE_PORT),
                            username=DATABASE_USER,
                            password=DATABASE_PASSWORD
                            )
    userdb = client["user-db"]
    users = userdb["users"]
    print('ok')
    return users

def edit_documents (request, document_id=None):
        id = document_id
        if request.method == 'POST':
            init_user = {"ID": 3}
            users = database()
            users.insert_one(init_user)
            return HttpResponse(id)
        elif request.method == 'GET':
            return HttpResponse(id)
        # r = requests.post('localhost:8000')
        
