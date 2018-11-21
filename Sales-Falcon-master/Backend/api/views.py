from django.shortcuts import render
from .models import (
    UserProfile,
    Customer,
    DeliveredMessage,
    MeetingNote,
    Company,)
from .serializers import (
    UserSerializer,
    UserProfileSerializer,
    UserDetailsSerializer,
    PotentialCustomerSerializer,
    CustomerSerializer,
    PutDeliveredMessageSerializer,
    FetchDeliveredMessageSerializer,
    SaveMeetingNotesSerializer,
    FetchMeetingNotesSerializer,
    CompanySerializer)
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.contrib.auth.models import User
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from rest_framework.parsers import FileUploadParser
from django.core.mail import send_mass_mail, send_mail, BadHeaderError
import random


class UserRegistration(APIView):
    """
    List the details of user
    """
    def post(self, request, format=None):
        user = request.data
        user['username'] = 'sf' + str(random.randint(1, 100)) + '_' + \
                           user['first_name'] + '_' + user['last_name']
        user_serializer = UserSerializer(data=user)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data)
        return Response(user_serializer.errors)


class UserDetails(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        user_details_serializer = UserProfileSerializer(data=request.data)
        if user_details_serializer.is_valid():
            user_details_serializer.save(owner=request.user)
            return Response(user_details_serializer.data)
        return Response(user_details_serializer.errors)

    def get(self, request, format=None):
        user = UserProfile.objects.get(owner=request.user)
        serializer = UserDetailsSerializer(user)
        return Response(serializer.data)


class Login(APIView):

    def post(self, request, format=None):
        email = request.data['email']
        username = User.objects.get(email=email).username

        password = request.data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({"message": "Success"})
        else:
            return Response({"message": "register please"})


class Logout(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        logout(request)
        return Response({"message": "Successfully logout"})


class FileUpload(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    parser_classes = (FileUploadParser,)

    def put(self, request, filename, format=None):
        file_obj = request.data['file']
        # TODO : Send to s3 bucket
        return Response(status=204)


class CustomerDetails(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        print(len(request.data))
        potential_customer_serializer = PotentialCustomerSerializer(data=request.data, many=True)
        if potential_customer_serializer.is_valid():
            potential_customer_serializer.save(owner=request.user)
            return Response(potential_customer_serializer.data)
        else:
            return Response(potential_customer_serializer.errors)

    def get(self, request, format=None):
        customers = Customer.objects.filter(owner=request.user)
        customer_details_serializer = CustomerSerializer(customers, many=True)
        return Response(customer_details_serializer.data)


class SendEmail(APIView):

    def post(self, request, format=None):

        sender = request.user.email
        message_type = request.data.get('message_type', '')
        message = request.data.get('message', '')
        receiver = request.data.get('receiver', '')
        subject = request.data.get('subject', '')
        if message_type == 'BULK' and subject and message and receiver:
            bulk_message = (subject, message, sender, receiver)
            try:
                send_mass_mail((bulk_message,))
            except BadHeaderError:
                return Response({"error": "Invalid Headers"})
        else:
            try:
                send_mail(subject, message, sender, receiver)
            except BadHeaderError:
                return Response({"error": "Invalid Headers"})

        message_serializer = PutDeliveredMessageSerializer(data=request.data)

        if message_serializer.is_valid():
            message_serializer.save(owner=request.user)
            return Response({"message": "success"})
        return Response({"message": "error", "error": message_serializer.errors})

    def get(self, request, format=None):
        messages = DeliveredMessage.objects.filter(owner=request.user)
        message_serializer = FetchDeliveredMessageSerializer(messages, many=True)
        return Response(message_serializer.data)


class MeetingNotesView(APIView):

    def post(self, request, format=None):
        potential_customer = Customer.objects.get(phone_no=request.data['customer']['phone_no'],
                                                  email=request.data['customer']['email'])
        request.data.pop('customer')
        serializer = SaveMeetingNotesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(customer=potential_customer)
            return Response(serializer.data)
        return Response(serializer.errors)

    def get(self, request, format=None):
        potential_customer = Customer.objects.get(phone_no=request.query_params['phone_no'])
        notes = MeetingNote.objects.get(customer=potential_customer)
        return Response(FetchMeetingNotesSerializer(notes).data)
