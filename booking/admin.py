from django.contrib import admin

# Register your models here.
from booking.models import User, ParkingSpace, Reservation

admin.site.register(User)
admin.site.register(Reservation)
admin.site.register(ParkingSpace)