from rest_framework import generics, permissions
from .models import Accounts
from .serializers import AccountSerializer, LoginSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import get_user_model
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

# Create your views here.
class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Accounts.objects.all()
    serializer_class = AccountSerializer


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


def verify_account(request, uidb64, token):
    UserModel = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserModel.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponseRedirect('https://hotel-booking-system-v1n6.onrender.com/login')
    else:
        return HttpResponse("Invalid verification link.")
    