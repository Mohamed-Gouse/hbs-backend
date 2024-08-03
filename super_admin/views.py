from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, permissions, viewsets
from hotel_side .models import Hotel, STATUS_CHOICES
from hotel_side.serializers import HotelSerializer, HotelStatusSerializer
from .serializers import UserSerializer
from auth_app.models import Accounts
from django.db.models import Q


class HotelsList(generics.ListAPIView):
    permission_classes = ([permissions.IsAuthenticated])
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

class HotelView(viewsets.ModelViewSet):
    permission_classes = ([permissions.IsAuthenticated])
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer


class StatusChoicesView(APIView):
    def get(self, request):
        choices = [{'value': choice[0], 'label': choice[1]} for choice in STATUS_CHOICES]
        return Response(choices)


class HotelStatusUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelStatusSerializer
    lookup_field = 'pk'

class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Accounts.objects.all().exclude(Q(is_superuser=True) | Q(role="admin"))

class DashboardStats(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.request.user

        hotels = Hotel.objects.all().count()
        hotels_accepted = Hotel.objects.filter(status='approved').count()
        hotels_rejected = Hotel.objects.filter(status='rejected').count()
        hotel_users = Accounts.objects.filter(role='hotel').exclude(pk=user.pk).count()
        public_users = Accounts.objects.filter(role='user').exclude(pk=user.pk).count()
        active_users = Accounts.objects.filter(is_active=True).exclude(pk=user.pk).count()

        datas = {
            "hotels": hotels,
            'hotels_accepted': hotels_accepted,
            'hotels_rejected': hotels_rejected,
            'hotel_users': hotel_users,
            'public_users': public_users,
            'active_users': active_users
        }

        return Response(datas)

