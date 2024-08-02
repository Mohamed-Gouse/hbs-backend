from rest_framework import serializers
from .models import Hotel, Document, Gallery, Feature, Room_type, Room, FAQ, Booking, Reservation
from interactions.models import Review
from auth_app.models import Accounts


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'

class HotelSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(read_only=True, source='document')
    class Meta:
        model = Hotel
        fields = '__all__'
        read_only_fields = ('slug', 'status', 'views', 'featured', )

class HotelStatusSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(read_only=True, source='document')
    class Meta:
        model = Hotel
        fields = '__all__'

class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = '__all__'

class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = '__all__'

class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room_type
        fields = '__all__'
        read_only_fields = ('slug',)

class RoomSerializer(serializers.ModelSerializer):
    room_type = serializers.PrimaryKeyRelatedField(queryset=Room_type.objects.all())
    room_type_details = RoomTypeSerializer(source='room_type', read_only=True)

    class Meta:
        model = Room
        fields = '__all__'

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    room = RoomSerializer(read_only=True)
    
    class Meta:
        model = Booking
        fields = "__all__"

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ('hotel', 'room', 'full_name', 'email', 'phone', 'total', 'check_in_date', 'check_out_date', 'guests')

class ReservationViewSerializer(serializers.ModelSerializer):
    room = RoomSerializer(read_only=True)

    class Meta:
        model = Reservation
        fields = '__all__'

class UserSerial(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = ['id', 'username']

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerial(read_only=True)
    hotel = HotelSerializer(read_only=True)
    class Meta:
        model = Review
        fields = '__all__'
