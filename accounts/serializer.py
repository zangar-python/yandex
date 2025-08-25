from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username','password']
    def create(self,validate_data):
        username = validate_data['username']
        password = validate_data['password']
        return User.objects.create_user(username=username,password=password)
    
    