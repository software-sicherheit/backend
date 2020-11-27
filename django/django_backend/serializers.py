from rest_framework import serializers
from .models import Document, User

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        # ('title','ersteller') -> ohneID
        fields =  '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # ('title','ersteller') -> ohneID
        fields =  '__all__'