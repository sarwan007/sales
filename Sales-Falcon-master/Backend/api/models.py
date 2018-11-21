from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

class Company(models.Model):
    name = models.CharField(max_length=20, blank=False)
    industry = models.TextField(max_length=500, blank=False)
    phone_no = models.CharField(max_length=13, blank=False)
    address = models.CharField(max_length=100, blank=False)
    city = models.TextField(max_length=100, blank=False)
    country = models.TextField(max_length=100, blank=False)
    state = models.TextField(max_length=100, blank=False)
    revenue = models.IntegerField(blank=False)
    email = models.EmailField(max_length=100, blank=False)
    stock_market = models.BooleanField(default=False)
    linkedin = models.URLField(max_length=100, blank=True, null=True)
    facebook = models.URLField(max_length=100, blank=True, null=True)
    website = models.URLField(max_length=200, blank=False)


class UserProfile(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=13, blank=False)
    profession = models.TextField(max_length=60, blank=False)
    experience = models.IntegerField(blank=False)
    linkedin = models.URLField(max_length=100, blank=True)
    facebook = models.URLField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=False)
    city = models.TextField(max_length=100, blank=False)
    country = models.TextField(max_length=100, blank=False)
    state = models.TextField(max_length=100, blank=False)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)


class Customer(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=False)
    address = models.CharField(max_length=100, blank=False)
    city = models.CharField(max_length=100, blank=False)
    country = models.TextField(max_length=100, blank=False)
    state = models.TextField(max_length=100, blank=False)
    linkedin = models.URLField(max_length=100, blank=True, null=True)
    facebook = models.URLField(max_length=100, blank=True, null=True)
    scoring = models.CharField(max_length=100, blank=False)
    phone_no = models.CharField(max_length=13, blank=False)
    email = models.EmailField(max_length=100, blank=False)
    website = models.URLField(max_length=200, blank=True, null=True)


class DeliveredMessage(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    message_type = models.CharField(max_length=100, choices=(("BULK", "bulk email"),
                                                             ("PERSONAL", "personal")),
                                    default=None, blank=False)
    receiver = ArrayField(models.CharField(max_length=500), blank=False)
    subject = models.CharField(max_length=200, blank=False)
    message = models.CharField(max_length=1000, blank=False)


class MeetingNote(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    flag = models.IntegerField(choices=((1, "Very Important"),
                                        (2, "Important"),
                                        (3, "Normal"),
                                        (4, "never mind")),
                               blank=False)
    notes = models.TextField(blank=False)
