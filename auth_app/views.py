from rest_framework import generics, permissions
from .models import Accounts
from .serializers import AccountSerializer, LoginSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

# Create your views here.
class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Accounts.objects.all()
    serializer_class = AccountSerializer


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

