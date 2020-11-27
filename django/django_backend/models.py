from djongo import models

class Document(models.Model):
    _id = models.ObjectIdField()
    title = models.CharField(max_length=20)
    ersteller = models.CharField(max_length=20)

class User(models.Model):
    # _id = models.ObjectIdField()
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=65)

'''
from django.db import models
from database.management import mongo_management as mm

print("Are we there yet?")
init_user = {"ID": 0,
             "name": "admin",
             "password": "admin",  # ToDo: Change xD
             "symmetricKey": "",
             "privateKey-PSS": "",
             "publicKey-PSS": "",
             "privateKey-OAEP": "",
             "publicKey-OAEP": "",
             "encryptedFilePath": ""}

mongoClient.printTest()
# mongoClient.add_user(init_user)
if (id == 1):
    print(mongoClient.return_user(0))

mongoClient = mm.MongoManagement()
'''

