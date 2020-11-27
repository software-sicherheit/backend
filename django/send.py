import requests

headers = {}
headers['Authorization'] = 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjA2NDc0NjEwLCJqdGkiOiJkMGVmYWY2ODQ3OGM0YzA1OWUxY2Q2MTljMjEwN2M1YiIsInVzZXJfaWQiOjJ9.Mn4NQ7ki8spiBb1rTrZza1kRKZJdWsE-xvCYldxiWuU'

r = requests.get('http://localhost:8000/api/v1/documents/', headers=headers)

print(r.text)