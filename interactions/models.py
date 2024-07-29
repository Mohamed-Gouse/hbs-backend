from django.db import models
from auth_app.models import Accounts
from hotel_side.models import Hotel, Room
from django.core.exceptions import ValidationError

# Create your models here.
class Selections(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField(null=True, blank=True)
    check_out = models.DateField(null=True, blank=True)
    total_days = models.IntegerField(null=True, blank=True)
    guest = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return f"{self.user.username} - {self.room.room_type.type}"

    def save(self, *args, **kwargs):
        if self.check_in and self.check_out:
            self.total_days = (self.check_out - self.check_in).days
        else:
            self.total_days = None

        # Check if the user has another active selection
        if self.status == 'active':
            active_selections = Selections.objects.filter(user=self.user, status='active').exclude(pk=self.pk)
            if active_selections.exists():
                if self.hotel and active_selections.exclude(hotel=self.hotel).exists():
                    raise ValidationError("You can only select rooms from the same hotel.")
                if not self.hotel:
                    raise ValidationError("Hotel must be specified for new selections.")

        super().save(*args, **kwargs)

class Wishlist(models.Model):
    user = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.hotel.name}"

class Review(models.Model):
    user = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    review = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.review}"
    
    def total_rating(self):
        return self.hotel.average_rating()
