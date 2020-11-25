from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from random import randint

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
            new_user = User(uuid = randint(2, 9999),
                            creation_time=datetime.date.today(),
                            username=data["username"],
                            password_hash=data["password_hash"],
                            symmetricKey = data["symmetricKey"],
                            privateKey_PSS = data["privateKey_PSS"],
                            publicKey_PSS = data["publicKey_PSS"],
                            privateKey_OAEP = data["privateKey_OAEP"],
                            publicKey_OAEP = ["publicKey_OAEP"]
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

            new_user.save()
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
            user_info = User()
            x = User.objects.filter(username__contains=username).values()
            return HttpResponse(x)
        except Exception as e:
            print(e)
            return HttpResponse(400)
    else:
        return HttpResponse(400)
