from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Accounts
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.conf import settings
from backend.tasks import send_verification_email

class AccountSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    photo = serializers.ImageField(read_only=True)

    class Meta:
        model = Accounts
        fields = ['username', 'full_name', 'email', 'photo', 'password', 'password2', 'role']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        user = Accounts.objects.create(
            full_name=validated_data['full_name'],
            username=validated_data['username'],
            email=validated_data['email'],
            role=validated_data['role'],
            is_active=False,
        )
        user.set_password(validated_data['password'])
        user.save()

        token_generator = default_token_generator
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)
        verification_url = f"{settings.BASE_URL}api/verify/{uid}/{token}"

        subject = f"Verification mail from HMS portal."
        message = f"{user.full_name} your account is created successfully. Kindly please verify your account with below provided link. \n\nVerification link: {verification_url} \n\nFor more query contact us through mail {settings.EMAIL_HOST_USER}."

        send_verification_email.delay(subject, message, [user.email])

        return user
    

class LoginSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({
            'user': {
                'full_name': self.user.full_name,
                'username': self.user.username,
                'email': self.user.email,
                'role': self.user.role,
            }
        })
        
        return data