from django.http import HttpResponse

import io
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
            return HttpResponse( mongoClient.return_user(id) ) # todo: austausch datenbakzugriff
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
        return HttpResponse(200)
    elif request.method == 'PUT':
        pass
    elif request.method == 'DELETE':
        id = int(id)
        mongoClient.delete_user(id)
        # Deletes all files of user aswell #todo: check for success and return depending response
        minioClient.purge_user(id)
        return HttpResponse(200)

def edit_documents (request, document_id=None):
        id = document_id
        if request.method == 'GET':
            if (id != None ):
                #id = int(id) # takes uuid and creates a list including all files that beginn with uuid/
                print("Document get file: GET x/file or get list of files from user x: GET documents/x")
                print(id)
                print("Minio generate object list: ")
                print(minioClient.generate_object_list(id))
                return HttpResponse( minioClient.generate_object_list(id) )
            else: #print(mongoClient.return_user(id)) #return user, get name,
                return HttpResponse(200) #mongoClient.return_user(id))

            print ("Testing Posts!")
            print ( request.get_host() )
            data = request.body.decode('UTF-8')
            print(data)
            jsondata = json.loads(data)
            print("nameOfJsondata: ")
            print(jsondata['filename'])

            # upload json form:
            # const document = {
            # id: this.documents.length + 1,
            # filename: file.name,
            # contentType: file.type,
            # size: file.size,
            # lastModifiedDate: file.lastModifiedDate,
            # blob: new Blob([file])
            # };

            print("Json Blob field: ")
            print(jsondata['blob'])
            #get uuid from jsondata, document_id or mongo_db?
            #buffer = io.StringIO( jsondata['blob'])
            buffer = io.BytesIO( bytes( jsondata['blob'], 'ascii') )
            print("The Printage of Buffer: ")
            print(buffer)
            minioClient.put_object(jsondata['id'], jsondata['filename'], buffer, int(jsondata['size']))

            # incase we use FORMs
            #print("Post: request.POST & request.FILES: ")
            #print (request.POST)
            #print (request.FILES)

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
            #minioClient.put_object(id,'formFileD', binary_data, sys.getsizeof(binary_data))
            #mongoClient.add_user(jsondata)
            return HttpResponse(id)
        elif request.method == 'PUT':
            pass
        elif request.method == 'DELETE':
            pass

