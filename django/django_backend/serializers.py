from rest_framework import serializers
from .models import MinioMeta
from django.contrib.auth.models import User

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


class MinioMetaSerializer(serializers.ModelSerializer):  
    class Meta:
        model = MinioMeta
        fields =  '__all__'