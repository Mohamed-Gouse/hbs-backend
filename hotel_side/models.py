from django.db import models
from auth_app.models import Accounts
import shortuuid
from django.utils.text import slugify
from django.core.exceptions import ValidationError

# Create your models here.
STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('processing', 'Processing'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

PAYMENT_STATUS = [
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('cancelled', 'Cancelled'),
        ('initiated', 'Initiated'),
        ('failed', 'Failed'),
        ('refunding', 'Refunding'),
        ('refunded', 'Refunded'),
        ('unpaid', 'Unpaid'),
        ('expired', 'Expired'),
    ]

DEFAULT_STATUS = 'requested'

class Hotel(models.Model):
    user = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='hotel_image', default="default.jpg")
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(blank=False, null=False, unique=True)
    facebook = models.URLField(max_length=1000, null=True, blank=True)
    instagram = models.URLField(max_length=1000, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    status = models.CharField(choices=STATUS_CHOICES, default=DEFAULT_STATUS, max_length=100)
    tags = models.CharField(max_length=255)
    views = models.IntegerField(default=0)
    featured = models.BooleanField(default=False)
    slug = models.SlugField(unique=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def average_rating(self):
        reviews = self.review_set.all()
        total_rating = sum(review.rating for review in reviews if review.rating is not None)
        review_count = reviews.count()
        return total_rating / review_count if review_count > 0 else 0
    
    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug == None:
            unique_key = shortuuid.ShortUUID().random(length=4)
            self.slug = slugify(self.name) + "-" + str(unique_key.lower())
        super(Hotel, self).save(*args, **kwargs)

class Document(models.Model):
    hotel = models.OneToOneField(Hotel, on_delete=models.CASCADE, related_name='document')
    license = models.FileField(upload_to='documents/')
    permit = models.FileField(upload_to='documents/')
    insurance = models.FileField(upload_to='documents/')
    certificate = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.hotel.name

class Gallery(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='gallery')
    image = models.FileField(upload_to='gallery')

    def __str__(self):
        return f"{self.hotel.name} - {self.image}"

class Feature(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='features')
    name = models.CharField(max_length=100, null=True, blank=True)

class Room_type(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='room_type')
    type = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    no_of_beds = models.PositiveIntegerField()
    room_capacity = models.PositiveIntegerField()
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.type
    
    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug == None:
            unique_key = shortuuid.ShortUUID().random(length=4)
            self.slug = slugify(self.type) + "-" + str(unique_key.lower())
        super(Room_type, self).save(*args, **kwargs)

class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    room_type = models.ForeignKey(Room_type, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=5)
    is_available = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['hotel', 'room_number'], name='unique_room_number_per_hotel')
        ]

    def __str__(self):
        return f"{self.room_type.type} - {self.room_number}"

class FAQ(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='faqs')
    quetion = models.CharField(max_length=255)
    answer = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.hotel.name} - {self.quetion}"

class Booking(models.Model):
    user = models.ForeignKey(Accounts, on_delete=models.SET_NULL, null=True, blank=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, null=True, blank=True)
    rooms = models.ManyToManyField(Room)
    full_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=100, choices=PAYMENT_STATUS, default='pending')
    before_discount = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    saved = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    total_days = models.PositiveIntegerField(default=1)
    guests = models.PositiveIntegerField(default=1)
    checked_in = models.BooleanField(default=False)
    checked_out = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    payment_intent = models.CharField(max_length=1000, null=True, blank=True)
    success_id = models.CharField(max_length=1000, null=True, blank=True)
    booking_id = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return f"{self.full_name} - {self.hotel.name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  
        if 'rooms' in kwargs:
            self.rooms.set(kwargs.pop('rooms'))

    @property
    def room_count(self):
        return self.rooms.count()

class Reservation(models.Model):
    user = models.ForeignKey(Accounts, on_delete=models.SET_NULL, null=True, blank=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=100, choices=PAYMENT_STATUS, default='pending')
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    total_days = models.PositiveIntegerField(default=1)
    guests = models.PositiveIntegerField(default=1)
    checked_in = models.BooleanField(default=False)
    checked_out = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    