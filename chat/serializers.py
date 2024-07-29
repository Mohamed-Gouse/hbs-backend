from rest_framework import serializers
from auth_app.models import Accounts

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = ['id', 'username', 'photo']
