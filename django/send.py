import requests
import jwt
# from rest_framework_jwt.utils import jwt_decode_handler

headers = {}
headers['Authorization'] = 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjA2NTg1MDU4LCJqdGkiOiJlNjNlZDY3YTI2MTI0YWNkYjE1MGJkYTVlZTI4YjlmMyIsInVzZXJfaWQiOjJ9.eYfHGgmfsH7g_csdaky7dUwJ_NLi6W20ClDfKDJ-F9U'

r = requests.get('http://localhost:8000/api/v1/documents/', headers=headers)
# decodedPayload = jwt.decode('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjA2NTg0NTUzLCJqdGkiOiI4ZTVjZWI1NTA4MTQ0NjhjODA0YTkyM2E3MGIzYTg0YyIsInVzZXJfaWQiOjJ9.49lwGEkAcmzdRsxz6W_TXshId1mtsD_oj4ZuCW_DGEA')
# header =  jwt.get_header(r)

print(r.text)