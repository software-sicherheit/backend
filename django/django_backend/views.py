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


from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .serializers import UserSerializer, RegisterSerializer, MinioMetaSerializer
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.models import User
from django.conf import settings
from .models import MinioMeta
from bson import ObjectId
import jwt
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .utils import generate_access_token
import psutil
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import permission_required

mongoClient = mon.MongoManagement()
minioClient = min.MinioManagement("accesskey", "secretkey")


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post (self, request, *args, **kwargs): 
        response = Response()
        username = request.data.get('username')
        password = request.data.get('password')
        if username == '':
            return Response(status = status.HTTP_406_NOT_ACCEPTABLE)
        try:
            user = User.objects.create_user(username=username, password=password)
        except:
            return Response(status = status.HTTP_409_CONFLICT)
        user = User.objects.filter(username=username).first()
        serialized_user = UserSerializer(user).data
        access_token = generate_access_token(user)
        # response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
        response.data = {
            'access_token': access_token,
        }

        return Response(response.data, status=status.HTTP_200_OK)
        # return Response(serializer.data, status = status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_view(request):    
    #permission_classes = (AllowAny,)
    User = get_user_model()
    username = request.data.get('username')
    password = request.data.get('password')
    if username == '' or password == '':
        return Response(status = status.HTTP_406_NOT_ACCEPTABLE)
    
    response = Response()
    user = User.objects.filter(username=username).first()
    if user is None or not user.check_password(password):
        return Response(status = status.HTTP_401_UNAUTHORIZED)

    serialized_user = UserSerializer(user).data
    access_token = generate_access_token(user)

    # response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
    response.data = {
        'access_token': access_token,
    }

    return Response(response.data, status=status.HTTP_200_OK)

@api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
def apiOverview(request):
    api_urls = {
        # Without #numbers the dict confuses the 'key':'value' pairs cause of similar keys
        '1. GET, POST, DELETE': 'api/v1/documents/',
        '2. GET, DELETE': 'api/v1/documents/<str:id>/',
        '3. GET, POST, DELETE': 'api/v1/users/',
        '4. GET, DELETE': 'api/v1/users/<str:id>/',
        }
    return Response(api_urls)

def get_uuid_from_jwt(request):
    authorization_header = request.headers.get('Authorization')
    access_token = authorization_header.split(' ')[1]
    payload = jwt.decode(
        access_token, settings.SECRET_KEY, algorithms=['HS256'])
    return str(payload['user_id']).zfill(4)

# /api/v1/documents/
@api_view(['GET','POST'])
# @permission_classes((IsAuthenticated, ))
def docList(request):
    if request.method == 'GET':
        try:
            return Response(minioClient.generate_object_list_json(get_uuid_from_jwt(request)))
        except:
            return Response(status=status.HTTP_404_NOT_FOUND) # Bad request
    elif request.method == 'POST': # Testwith: {"id":"0011","filename":"bananenbrotsalat","contentType":"file.type","size":"8","lastModifiedDate":"lastModifiedDate","blob":"blobdata"}
        try:
            jsondata = json.loads(request.body.decode('UTF-8'))
            buffer = io.BytesIO(bytes(jsondata['blob'], 'ascii'))

            minioClient.put_object( get_uuid_from_jwt(request), jsondata['filename'], buffer, int(jsondata['size']), str(jsondata['contentType']))
            return Response(201)  # c reate d
        except Exception as e:
            return Response(status=status.HTTP_404_NOT_FOUND) #Bad request cause of invalid syntax

# api/v1/documents/<str:id> # downloads and deletes specific files from database
@api_view(['GET','DELETE'])
@permission_classes((IsAuthenticated, ))
def docDetail(request, id):
    if request.method == 'GET':
        try:
            return Response( minioClient.get_file( get_uuid_from_jwt(request), str(id) ) )
        except:
            return Response(400)
    elif request.method == 'DELETE':
        try:
            minioClient.remove_file( get_uuid_from_jwt(request), str(id) )
            return Response(200)
        except:
            return Response(400)
        return HttpResponse(200)

# api/v1/users/
@api_view(['GET','POST', 'DELETE'])
# @permission_classes((IsAuthenticated, ))
def userList(request):
    if request.method == 'GET':
        uuid = get_uuid_from_jwt(request)
        # minioMeta = MinioMeta.objects.filter(uuid=uuid)
        minioMeta = MinioMeta.objects.all()
        if minioMeta is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MinioMetaSerializer(minioMeta, many=False)
        serializer.data,     
        return Response(status=status.HTTP_200_OK) 
    elif request.method == 'POST':
        uuid = get_uuid_from_jwt(request)
        passwordKey = request.data.get('passwordKey')
        oaep = request.data.get('rsaOAEP')
        pss = request.data.get('rsaPSS')
        dataNameKey = request.data.get('dataNameKey')      
        try:
            minioMeta = MinioMeta(uuid=uuid, passwordKey=passwordKey, oaep=oaep, pss=pss, dataNameKey=dataNameKey)
            minioMeta.save()
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        uuid = get_uuid_from_jwt(request)
        user = User.objects.get(id=uuid)
        user.delete()
        ## Redirect
        return Response (status=status.HTTP_200_OK)

# api/v1/admin/users/
# @staff_member_required
@api_view(['GET'])
# @permission_required('is_superuser')
# @staff_member_required
def userAll(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# api/v1/admin/users/<user_id>
# @staff_member_required
#@permission_required('is_superuser')
@api_view(['DELETE'])
def userDelete(request, id):
    # permission_classes = (IsAdminUser,)
    if request.method == 'DELETE':
        uuid = get_uuid_from_jwt(request)
        resp = {}
        try:
            miniometa = MinioMeta.objects.filter(uuid=id)
            miniometa.delete()
            resp = resp + {'MinioMeta':'pass'}
        except Exception as e:
            resp = resp + {'MinioMeta':e}
        try:
            user = User.objects.get(id=id)
            user.delete()
            resp = resp + {'User':'pass'}
        except Exception as e:
            resp = resp + {'User':e}
        try:
            minioClient.purge_user(int(id))  # Deletes all files of given user
            resp = resp + {'MinioData':'pass'}
        except Exception as e: 
            resp = resp + {'MinioData':e}
        return HttpResponse(str(resp))


@api_view(['GET'])
@staff_member_required
def statistic(request):
    statistics= {
            'cpuUsage': int( psutil.cpu_percent()),  # to be filled in views from jwt
            'ramUsage': int( psutil.virtual_memory().percent ),
            'diskUsage':int( psutil.disk_usage("/").percent ) ,
            'swapUsage':int( psutil.swap_memory().percent ) ,
            'inboundTraffic':int( psutil.net_io_counters().bytes_recv),
            'outboundTraffic':int( psutil.net_io_counters().bytes_sent)
        }
    return HttpResponse( str(statistics) )


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