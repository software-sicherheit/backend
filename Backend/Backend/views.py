from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from random import randint, choice

import datetime
import json


@csrf_exempt
def create_user(request):
    if request.method == 'GET':
        return HttpResponse(400)
    elif request.method == 'POST':
        try:
            # Create new user
            data = json.loads(request.body)

            # Get all existing uuids
            uuids = User.objects.filter().values('uuid')
            uuid_list = [uuid['uuid'] for uuid in uuids]

            # Generate all possible uuids
            available_uuids = [i for i in range(2, 10000) if i not in uuid_list]

            # Check if any uuids are available
            if not available_uuids:
                return HttpResponse(500)

            # Take random uuid
            random_uuid = choice(available_uuids)

            print(uuid_list)
            print(random_uuid)

            random_uuid = randint(2, 9999)

            new_user = User(uuid=random_uuid,
                            creation_time=datetime.date.today(),
                            username=data["username"],
                            password_hash=data["password_hash"],
                            symmetricKey = data["symmetricKey"],
                            privateKey_PSS = data["privateKey_PSS"],
                            publicKey_PSS = data["publicKey_PSS"],
                            privateKey_OAEP = data["privateKey_OAEP"],
                            publicKey_OAEP = data["publicKey_OAEP"],
                            minio_path = data["minio_path"]
                            )

            '''
            CURL POST-Request for test purpose
            
            curl -d '{"username":"new_user",
                      "password_hash":{"salt": "random_salt", "hash": "ee64f6db5b05dceffe9068f85232901a"},
                      "symmetricKey": "example_key_sym",
                      "privateKey_PSS": "example_key_priv_PSS",
                      "publicKey_PSS": "example_key_pub_PSS",
                      "privateKey_OAEP": "example_key_priv_OAEP",
                      "publicKey_OAEP": "example_key_pub_OAAEP"}'
                      -H "Content-Type: application/json" -X POST http://127.0.0.1:8000/users/
            
            '''

            new_user.save(force_insert=True)
            return HttpResponse(200)

        except Exception as e:
            # Log e
            print(e)
            return HttpResponse(400)

    else:
        return HttpResponse(400)


@csrf_exempt
def get_user(request, username=''):
    if username == '':
        return HttpResponse(400)
    if request.method == 'POST':
        return HttpResponse(400)
    elif request.method == 'GET':
        try:
            data = User.objects.filter(username__contains=username).values()
            return HttpResponse(data)

        except Exception as e:
            print(e)
            return HttpResponse(400)
    else:
        return HttpResponse(400)


@csrf_exempt
def change_password(request):
    if request.method == 'GET':
        return HttpResponse(400)
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)

            # iterate over JSON and update the values in the database
            upd_user = User(uuid=data["uuid"],
                            creation_time=datetime.date.today(),
                            username=data["username"],
                            password_hash=data["password_hash"],
                            symmetricKey = data["symmetricKey"],
                            privateKey_PSS = data["privateKey_PSS"],
                            publicKey_PSS = data["publicKey_PSS"],
                            privateKey_OAEP = data["privateKey_OAEP"],
                            publicKey_OAEP = data["publicKey_OAEP"],
                            minio_path = data["minio_path"]
                            )

            '''
            CURL POST-Request for test purpose
            
            curl -d '{"uuid": "1234"
                      "username":"new_user",
                      "password_hash":{"salt": "random_salt", "hash": "ee64f6db5b05dceffe9068f85232901a"},
                      "symmetricKey": "example_key_sym",
                      "privateKey_PSS": "example_key_priv_PSS",
                      "publicKey_PSS": "example_key_pub_PSS",
                      "privateKey_OAEP": "example_key_priv_OAEP",
                      "publicKey_OAEP": "example_key_pub_OAAEP"}'
                      -H "Content-Type: application/json" -X POST http://127.0.0.1:8000/users/update/
            
            '''

            upd_user.save(force_update=True)
            return HttpResponse(200)

        except Exception as e:
            print(e)
            return HttpResponse(500)
    else:
        return HttpResponse(400)
