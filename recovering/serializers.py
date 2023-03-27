from abc import ABC

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from recovering.models import *


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        token['username'] = user.username
        member = user

        return token


class VersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Version
        fields = ['id', 'title', 'author', 'audio', 'saloon', 'lyrics', 'created']


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id', 'username', 'password', 'type', 'first_name', 'last_name',
                  'created', 'email', 'city', 'neighborhood',
                  'phone_number']


"""class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id', 'username', 'password', 'type', 'first_name', 'last_name',
                  'created', 'email', 'city', 'neighborhood',
                  'phone_number']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        member = Member.objects.create(
            username=validated_data['username'],
            password=validated_data['password'],
            type=validated_data['type'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            city=validated_data['city'],
            neighborhood=validated_data['neighborhood'],
            phone_number=validated_data['phone_number']
        )

        return member"""


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['id', 'username', 'first_name', 'last_name', 'password',
                  'created', 'email']


class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = ['id', 'creator', 'name', 'status', 'created', 'members']


class ValidatedCommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = ['id', 'creator', 'name', 'status', 'created']


class ComitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Comity
        fields = ['id', 'community', 'members']


class SaloonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Saloon
        fields = ['id', 'title', 'author', 'community', 'supervisor', 'state', 'created']


class CommunityValidationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityValidation
        fields = ['id', 'validator', 'community']


class FavoritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = ['id', 'member', 'version']


class FinalVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinalVersion
        fields = ['id', 'version']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['author', 'content', 'saloon']
