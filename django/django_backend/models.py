from djongo import models

class Document(models.Model):
    _id = models.ObjectIdField()
    filename = models.CharField(max_length=40)
    contentType = models.CharField(max_length=40)
    size = models.DecimalField(..., max_digits=10, decimal_places=2)
    lastmodifieddate = models.CharField(max_length=40)
    blob = models.CharField(max_length=1048576) # 10 Mb
    #'{"id":"11","filename":"robert","contentType":"file.type","size":"8",' \
    #'"lastModi$iedDate":"file.lastModifiedDate","blob":"blobdata"}'


    def __str__(self):
        return self.title

class User(models.Model):
    _id = models.ObjectIdField()
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    
    def __str__(self):
        return self.username

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

