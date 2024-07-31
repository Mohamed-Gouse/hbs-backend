from rest_framework import serializers
from auth_app.models import Accounts

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = ['id', 'username', 'full_name', 'is_active', 'email', 'photo']