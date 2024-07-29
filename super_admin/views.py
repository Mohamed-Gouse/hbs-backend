from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, permissions, viewsets
from hotel_side .models import Hotel, STATUS_CHOICES
from hotel_side.serializers import HotelSerializer, HotelStatusSerializer


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
