from django.http import HttpResponse

import io
import os
import sys
import json
sys.path.append(os.getcwd())
from database.management import mongo_management as mon
from minio_src import minio_management as min

from rest_framework import generics, permissions, mixins, status, exceptions
from rest_framework.parsers import JSONParser 


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import DocumentSerializer, UserSerializer, RegisterSerializer
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.models import User
from django.conf import settings
from .models import Document
from bson import ObjectId
import jwt
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
# from . import backends
from .utils import generate_access_token, generate_refresh_token

mongoClient = mon.MongoManagement()
minioClient = min.MinioManagement("accesskey", "secretkey")


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post (self, request, *args, **kwargs): 
        response = Response()
        username = request.data.get('username')
        password = request.data.get('password')
        if (username is None) or (password is None):
            return Response(status = status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=username, password=password)
        user = User.objects.filter(username=username).first()
        serialized_user = UserSerializer(user).data
        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)
        response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
        response.data = {
            'access_token': access_token,
            'user_id': serialized_user['id'],
        }
        return response
        # return Response(serializer.data, status = status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_view(request):
    permission_classes = (IsAuthenticated,)
    User = get_user_model()
    username = request.data.get('username')
    password = request.data.get('password')
    response = Response()
    if (username is None) or (password is None):
        raise exceptions.AuthenticationFailed(
            'username and password required')

    user = User.objects.filter(username=username).first()
    if(user is None):
        raise exceptions.AuthenticationFailed('user not found')
    if (not user.check_password(password)):
        raise exceptions.AuthenticationFailed('wrong password')

    serialized_user = UserSerializer(user).data

    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)

    response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
    response.data = {
        'access_token': access_token,
        'user_id': serialized_user['id'],
    }

    return response
'''
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Add extra responses here
        data['username'] = self.user.username
        data['groups'] = self.user.groups.values_list('name', flat=True)
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer     
'''

@api_view(['GET'])
def apiOverview(request):
    permission_classes = (IsAuthenticated,)
    api_urls = {
        # Without #numbers the dict confuses the 'key':'value' pairs cause of similar keys
        '1. GET, POST, DELETE': 'api/v1/documents/',
        '2. GET, DELETE': 'api/v1/documents/<str:id>/',
        '3. GET, POST, DELETE': 'api/v1/users/',
        '4. GET, DELETE': 'api/v1/users/<str:id>/',
        }
    return Response(api_urls)

# /api/v1/documents/
@api_view(['GET','POST'])
def docList(request):
    if request.method == 'GET':
        try:
            uuid = 11
            uuid = str(uuid).zfill(4) # todo: get uuid from jwt token
            return Response( minioClient.generate_object_list_json())#uuid) )
        except:
            return Response( HttpResponse(400) ) # Bad request
    elif request.method == 'POST': # Testwith: {"id":"0011","filename":"bananenbrotsalat","contentType":"file.type","size":"8","lastModifiedDate":"lastModifiedDate","blob":"blobdata"}
        try:
            jsondata = json.loads(request.body.decode('UTF-8'))
            buffer = io.BytesIO(bytes(jsondata['blob'], 'ascii'))
            uuid = jsondata['id'] # todo: get uuid from jwt
            uuid = str(uuid).zfill(4)
            minioClient.put_object( str(uuid), jsondata['filename'], buffer, int(jsondata['size']))
            return Response(201)  # created
        except:
            return Response(400) #Bad request cause of invalid syntax

# api/v1/documents/<str:id> # downloads and deletes specific files from database
@api_view(['GET','DELETE'])
def docDetail(request, id):
    permission_classes = (IsAuthenticated,)
    if request.method == 'GET':
        try:
            print("ID:")
            print(id)
            uuid = 11 # todo: get from jwt token # Path is uudi/id
            uuid = str(uuid).zfill(4) # todo: get uuid from jwt token
            return Response( minioClient.get_file( str(uuid), str(id) ) )
        except:
            return Response(400)
    elif request.method == 'DELETE':
        try:
            uuid = "0011" # todo: get from jwt token
            uuid = str(uuid).zfill(4)
            minioClient.remove_file( str(uuid), str(id) )
            return Response(200)
        except:
            Response(400)
        return HttpResponse(200)

# api/v1/users/
@api_view(['GET','POST','DELETE'])
def userList(request):
    permission_classes = (IsAuthenticated,)
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many = True)
        return Response(serializer.data)
    elif request.method == 'POST':
        # serializer = UserSerializer(data=request.data)
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.create_user(username=username, password=password)
        print (username, password)
        return HttpResponse("angelegt")
    elif request.method == 'DELETE':
        users = User.objects.all()
        users.delete()
        return HttpResponse("deleted")

# api/v1/users/<user_id>
@api_view(['GET','DELETE'])
def userDetail(request, id):
    if request.method == 'GET':
        users = User.objects.get(_id=ObjectId(id))
        serializer = UserSerializer(users, many=False)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        user = User.objects.get(_id=ObjectId(id))
        minioClient.purge_user(int(id))  # Deletes all files of user
        user.delete()
        return HttpResponse("Dokument gelöscht")

    # End Land #

'''
doc_data = JSONParser().parse(request)
serializer = DocumentSerializer(data=doc_data)
if serializer.is_valid():
    serializer.save()
return Response(serializer.data)
'''
'''
#todo: try catching

def response2json(http_response):
    data = http_response.body.decode('UTF-8')
    jsondata = json.loads(data)
    return jsondata

# Here: user_id == uuid
def edit_users(request, user_id=None):

    if request.method == 'GET':
        if (user_id != None):
            return HttpResponse( mongoClient.return_user( int(user_id)) ) # todo: austausch datenbakzugriff
        else:
            return HttpResponse( 200 )
    elif request.method == 'POST':
        mongoClient.add_user( response2json(request) )
        return HttpResponse(200)
    elif request.method == 'PUT':
        pass
    elif request.method == 'DELETE':
        id = int(id)
        mongoClient.delete_user(id)
        minioClient.purge_user(int(user_id)) # Deletes all files of user aswell
        return HttpResponse(200)

# if needed: get UUID from jwt token! document_id is filename
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
'''