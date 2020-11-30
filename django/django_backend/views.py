from django.http import HttpResponse

import io
import os
import sys
import json
sys.path.append(os.getcwd())
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
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import user_passes_test
from django.core import serializers

minioClient = min.MinioManagement(os.environ.get('MINIO_ACCESS_KEY'), os.environ.get('MINIO_SECRET_KEY'))


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
def docList(request):
    try:
        uuid = get_uuid_from_jwt(request)
    except:
        return Response(status=status.HTTP_403_FORBIDDEN)
    user = User.objects.get(id=uuid)
    if not user.is_authenticated:
        return Response (status=status.HTTP_403_FORBIDDEN)
    if request.method == 'GET':
        try:
            return Response(minioClient.generate_object_list_json(get_uuid_from_jwt(request)))
        except:
            return Response(status=status.HTTP_404_NOT_FOUND) # Bad request
    elif request.method == 'POST': # Testwith: {"id":"0011","filename":"bananenbrotsalat","contentType":"file.type","size":"8","lastModifiedDate":"lastModifiedDate","blob":"blobdata"}
        try:
            jsondata = json.loads(request.body.decode('UTF-8'))
            buffer = io.BytesIO(bytes(jsondata['blob'], 'ascii'))

            minioClient.put_object( get_uuid_from_jwt(request), jsondata['filename'],
                                    buffer, int(jsondata['size']), str(jsondata['contentType']))
            return Response(201)  # c reate d
        except:
            return Response(status=status.HTTP_404_NOT_FOUND) #Bad request cause of invalid syntax

# api/v1/documents/<str:id> # downloads and deletes specific files from database
@api_view(['GET','DELETE'])
def docDetail(request, id):
    try:
        uuid = get_uuid_from_jwt(request)
    except:
        return Response(status=status.HTTP_403_FORBIDDEN)
    user = User.objects.get(id=uuid)
    if not user.is_authenticated:
        return Response (status=status.HTTP_403_FORBIDDEN)
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
def userList(request):
    try:
        uuid = get_uuid_from_jwt(request)
    except:
        return Response(status=status.HTTP_403_FORBIDDEN)
    user = User.objects.get(id=uuid)
    if not user.is_authenticated:
        return Response (status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'GET':
        minioMeta = MinioMeta.objects.filter(uuid=uuid)
        # minioMeta = MinioMeta.objects.all()
        if minioMeta is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        #serializer = MinioMetaSerializer.restore_object(minioMeta)
        data = serializers.serialize('json',minioMeta)
        data = data[63:-2]
        data = json.loads(data)
        return Response(data, status=status.HTTP_200_OK) 
        
    elif request.method == 'POST':
        passwordKey = request.data.get('passwordKey')
        oaep = request.data.get('rsaOAEP')
        pss = request.data.get('rsaPSS')
        dataNameKey = request.data.get('dataNameKey')      
        try:
            minioMeta = MinioMeta(uuid=uuid, passwordKey=passwordKey, rsaOAEP=oaep, rsaPSS=pss, dataNameKey=dataNameKey)
            minioMeta.save()
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        minioClient.purge_user(str(uuid))
        user = User.objects.get(id=uuid)
        user.delete()
        return Response (status=status.HTTP_200_OK)

# api/v1/admin/users/
@api_view(['GET'])
def userAll(request):
    try:
        uuid = get_uuid_from_jwt(request)
    except:
        return Response(status=status.HTTP_403_FORBIDDEN)
    user = User.objects.get(id=uuid)
    if not user.is_superuser:
        return Response (status=status.HTTP_403_FORBIDDEN)
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# api/v1/admin/users/<user_id>
@api_view(['DELETE'])
def userDelete(request, id):
    try:
        uuid = get_uuid_from_jwt(request)
    except:
        return Response(status=status.HTTP_403_FORBIDDEN)
    user = User.objects.get(id=uuid)
    if not user.is_superuser and not request.user.is_authenticated:
        return Response (status=status.HTTP_403_FORBIDDEN)
    if request.method == 'DELETE':
        resp = {}
        try:          
            miniometa = MinioMeta.objects.filter(uuid=id)
            if len(miniometa) == 0:
                resp['MinioMeta'] = 'No entry found'
            else:
                miniometa.delete()
                resp ['MinioMeta'] = 'pass'
        except Exception as e:
            resp ['MinioMeta'] = str(e)
        try:
            minioClient.purge_user(int(id))  # ToDo: "unsupported operand type(s) for +: 'int' and 'str'"
            resp ['MinioData'] = 'pass'
        except Exception as e: 
            resp ['MinioData'] = str(e)
        try:
            user = User.objects.get(id=id)
            if user is None:
                resp['User'] = 'No user found'
            else:
                user.delete()
                resp ['User'] = 'pass'
        except Exception as e:
            resp ['User'] = str(e)
        try:
            minioClient.purge_user(str(id).zfill(4))  # ToDo: "unsupported operand type(s) for +: 'int' and 'str'"
            resp = resp + {'MinioData':'pass'}
        except Exception as e: 
            resp ['MinioData'] = str(e)

        return HttpResponse(str(resp))

# api/v1/statistics/overview/
@api_view(['GET'])
def statistic(request):
    try:
        uuid = get_uuid_from_jwt(request)
    except:
        return Response(status=status.HTTP_403_FORBIDDEN)
    user = User.objects.get(id=uuid)
    if not user.is_superuser:
        return Response (status=status.HTTP_403_FORBIDDEN)
    #dict.keys()

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