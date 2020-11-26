from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

import io
import json

from minio_src import minio_management as min

from .models import *

minioClient = min.MinioManagement("accesskey", "secretkey")

'''
dependencies needed on server: pymongo, environs
'''

@csrf_exempt
def response2json(http_response):
    data = http_response.body.decode('UTF-8')
    jsondata = json.loads(data)
    return jsondata

# Here: user_id == uuid
@csrf_exempt
def edit_users(request, user_id=None):

    if request.method == 'GET':
        if (user_id != None):
            #return HttpResponse( mongoClient.return_user( int(user_id)) ) # todo: austausch datenbakzugriff
            return
        else:
            return HttpResponse( 200 )
    elif request.method == 'POST':
        #mongoClient.add_user( response2json(request) )
        return HttpResponse(200)
    elif request.method == 'PUT':
        pass
    elif request.method == 'DELETE':
        id = int(id)
        #mongoClient.delete_user(id)
        minioClient.purge_user(int(user_id)) # Deletes all files of user aswell
        return HttpResponse(200)

# if needed: get UUID from jwt token! document_id is filename
@csrf_exempt
def edit_documents (request, document_id=None):
        id = document_id
        if request.method == 'GET':

            # work in progress #
            if (id != None ):
                #id = int(id) # takes uuid and creates a list including all files that beginn with uuid/
                print("Document get file: GET x/file or get list of files from user x: GET documents/x")
                print(id)
                print("Minio generate object list: ")
                print(minioClient.generate_object_list(id))
                return HttpResponse( minioClient.generate_object_list(id) )
            else: #print(mongoClient.return_user(id)) #return user, get name,
                return HttpResponse(200) #mongoClient.return_user(id))

            data = request.body.decode('UTF-8')
            jsondata = json.loads(data)

            buffer = io.BytesIO( bytes( jsondata['blob'], 'ascii') )
            minioClient.put_object(jsondata['id'], jsondata['filename'], buffer, int(jsondata['size']))
            return HttpResponse(id)
        elif request.method == 'PUT':
            pass
        elif request.method == 'DELETE':
            pass





























def baum(request):
    b = Baum(anzahl_aeste=10)
    b.save()
