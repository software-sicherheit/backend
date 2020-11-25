from django.http import HttpResponse

import os
import sys
import json
sys.path.append(os.getcwd())
from database.management import mongo_management as mon
from minio_src import minio_management as min


mongoClient = mon.MongoManagement()
minioClient = min.MinioManagement("accesskey", "secretkey")

'''
dependencies needed on server: pymongo, environs
django forbids relative imports above top level
another relative imports problem: our pwd in docker will be changed to "/code"
if we want to use multiple buckets in minio ne need to store the bucket_id in the mongo_database
'''
# print("Working Dir: ")
# print(os.getcwd())

# users/ & users/{id}
def edit_users(request, user_id=None):
    id = user_id
    if request.method == 'GET': # return by name aswell?
        if (id != None):
            id = int(id)
            #print(type(id))
            return HttpResponse( mongoClient.return_user(id) )
        else:
            return HttpResponse( 200 )
    elif request.method == 'POST':
        # Send users like this:
        # Don't forget to specifiy the Content-Type
        # curl --header Content-Tpye:application/json
        #      --request POST --data '{"ID": 1,"name": "admin","password": "admin",
        #      "symmetricKey": "","privateKey-PSS": "","publicKey-PSS": "",
        #      "privateKey-OAEP": "","publicKey-OAEP": "","encryptedFilePath": ""}'
        #      http://127.0.0.1:8000/users/
        data = request.body.decode('UTF-8')
        print(data)
        jsondata = json.loads(data)
        print("name: ")
        print(jsondata['name'])
        mongoClient.add_user(jsondata)
        return HttpResponse(1)
    elif request.method == 'PUT':
        pass
    elif request.method == 'DELETE':
        id = int(id)
        mongoClient.delete_user(id)
        # Deletes all files of user aswell | need to create mini put first to define pathstructure
        minioClient.purge_user(id)
        pass

def edit_documents (request, document_id=None):
        id = document_id
        if request.method == 'GET':
            if (id != None ):
                id = int(id)
            # takes uuid and creates a list including all files that beginn with uuid/
            minioClient.generate_object_list(id)
            #print(mongoClient.return_user(id)) #return user, get name,
            return HttpResponse(200) #mongoClient.return_user(id))
        elif request.method == 'POST':
            #For processing conventional form data, use HttpRequest.POST
            binary_data = request.body
            #print ("Testing Posts!")
            #print ( request.get_host() )
            #data = request.body.decode('UTF-8')
            #print(data)
            #jsondata = json.loads(data)
            #print("name: ")
            #print(jsondata['name'])

            print("Post: request.POST & request.FILES: ")
            print (request.POST)
            print (request.FILES)

            #Post: request.POST & request.FILES:                                     │
            #< QueryDict: {} >                                                         │
            #< MultiValueDict: {'fileupload': [ < InMemoryUploadedFile: fileForTestUploa│
            #d.txt(text / plain) >]} >

            #^ todo: wrap into right dataformat and pass onto miniClient.put_object

#            form = DocumentForm(request.POST, request.FILES)
#            if form.is_valid():
#                newdoc = Document(docfile=request.FILES['docfile'])

            # - Start here! - this needs work
            # todo: handle document/id handeling, string vs char vs int etc.
            minioClient.put_object(id,'formFileD', binary_data, sys.getsizeof(binary_data))
            #mongoClient.add_user(jsondata)
            return HttpResponse(id)
        elif request.method == 'PUT':
            pass
        elif request.method == 'DELETE':
            pass

