from django.contrib import admin
from .models import Hotel, Document, Gallery, Feature, Room_type, Room, FAQ, Booking, Reservation

class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'state', 'country', 'status', 'views', 'featured')
    search_fields = ('name', 'city', 'state', 'country')
    list_filter = ('status', 'featured')
    list_editable = ('status', 'featured', )
    prepopulated_fields = {'slug': ('name',)}

class DocumentAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'uploaded_at')
    search_fields = ('hotel__name',)
    list_filter = ('uploaded_at',)

class GalleryAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'image')
    search_fields = ('hotel__name',)

class FeatureAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'name')
    search_fields = ('hotel__name', 'name')

class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'type', 'price', 'no_of_beds', 'room_capacity')
    search_fields = ('hotel__name', 'type')
    list_filter = ('hotel',)
    prepopulated_fields = {'slug': ('type',)}

class RoomAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'room_type', 'room_number', 'is_available')
    search_fields = ('hotel__name', 'room_type__type', 'room_number')
    list_filter = ('hotel', 'room_type', 'is_available')

class FAQAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'quetion', 'date')
    search_fields = ('hotel__name', 'quetion')
    list_filter = ('date',)

class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'hotel', 'check_in_date', 'check_out_date', 'total_days', 'guests', 'payment_status', 'is_active')
    search_fields = ('user__username', 'hotel__name', 'room')
    list_filter = ('payment_status', 'is_active', 'check_in_date', 'check_out_date')

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'hotel', 'check_in_date', 'check_out_date', 'total_days', 'guests', 'payment_status', 'is_active')
    search_fields = ('user__username', 'hotel__name', 'room')
    list_filter = ('payment_status', 'is_active', 'check_in_date', 'check_out_date')

admin.site.register(Hotel, HotelAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(Room_type, RoomTypeAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Reservation, ReservationAdmin)
