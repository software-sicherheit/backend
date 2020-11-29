from rest_framework import serializers
# from .models import Document
from django.contrib.auth.models import User

'''
class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        # ('title','ersteller') -> ohneID
        fields =  '__all__'
'''

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','password')
        extra_kwargs = {
            'password':{'write_only':True},
        }

class UserSerializer(serializers.ModelSerializer):  
    class Meta:
        model = User
        fields =  '__all__'