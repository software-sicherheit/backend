# from djongo import models
from django.db import models
#from django_mysql.models import JSONField
import jsonfield

'''
class Document(models.Model):
    #id = models.ObjectIdField()
    # id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=20)
    ersteller = models.CharField(max_length=20)
'''
'''
class User(models.Model):
    # _id = models.ObjectIdField()
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=65)
'''

class MinioMeta(models.Model):
    uuid = models.CharField(max_length=10, primary_key=True)
    passwordKey = jsonfield.JSONField()
    rsaOAEP = jsonfield.JSONField()
    rsaPSS = jsonfield.JSONField()
    dataNameKey = jsonfield.JSONField()

    objects = models.Manager()

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

