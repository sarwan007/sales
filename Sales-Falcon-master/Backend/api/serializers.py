from rest_framework import serializers
from .models import ( Company,
                      UserProfile,
                      Customer,
                      DeliveredMessage,
                      MeetingNote, )
from django.contrib.auth.models import User


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('name', 'industry', 'revenue', 'email', 'phone_no',
                  'address', 'city', 'state', 'country', 'website')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        extra_kwargs = {'password': {'write_only': True}}
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password')

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = UserProfile
        fields = ('owner', 'mobile', 'profession', 'experience', 'address', 'city',
                  'state', 'country', 'company', 'facebook', 'linkedin')

    def create(self, validated_data):
        company_details = validated_data.pop('company')
        if Company.objects.filter(name=company_details['name'], city=company_details['city']).exists():
            company = Company.objects.get(name=company_details['name'], city=company_details['city'])
            user = UserProfile.objects.create(company=company, **validated_data)
            return user
        company = Company.objects.create(**company_details)
        user = UserProfile.objects.create(company=company, **validated_data)
        return user


class UserDetailsSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    owner = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ('owner', 'mobile', 'profession', 'experience', 'address', 'city',
                  'state', 'country', 'company')


class CustomerSerializer(serializers.ModelSerializer):
    owner = UserSerializer()

    class Meta:
        model = Customer
        fields = ('owner', 'name', 'address', 'city',
                  'state', 'country', 'phone_no', 'email',
                  'linkedin', 'facebook', 'scoring', 'website')


class PotentialCustomerSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Customer
        fields = ('id', 'owner', 'name', 'address', 'city',
                  'state', 'country', 'phone_no', 'email',
                  'linkedin', 'facebook', 'scoring', 'website')


class PutDeliveredMessageSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = DeliveredMessage
        fields = ('owner', 'message_type', 'receiver', 'subject', 'message')


class FetchDeliveredMessageSerializer(serializers.ModelSerializer):
    owner = UserSerializer()

    class Meta:
        model = DeliveredMessage
        fields = ('owner', 'message_type', 'receiver', 'subject', 'message')


class SaveMeetingNotesSerializer(serializers.ModelSerializer):
    customer = serializers.ReadOnlyField(source='customer.id')

    class Meta:
        model = MeetingNote
        fields = ('customer', 'flag', 'notes')


class FetchMeetingNotesSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()

    class Meta:
        model = MeetingNote
        fields = ('customer', 'flag', 'notes')
