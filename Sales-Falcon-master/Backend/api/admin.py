from django.contrib import admin
from .models import Company, UserProfile, Customer, DeliveredMessage, MeetingNote

# Register your models here.
admin.site.register(Company)
admin.site.register(UserProfile)
admin.site.register(Customer)
admin.site.register(DeliveredMessage)
admin.site.register(MeetingNote)
