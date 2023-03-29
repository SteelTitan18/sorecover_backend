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
