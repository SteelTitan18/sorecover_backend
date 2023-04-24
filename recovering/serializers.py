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
        fields = ['id', 'title', 'creator', 'audio', 'saloon', 'lyrics', 'created']


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['username', 'password', 'type', 'first_name', 'last_name',
                  'created', 'email', 'city', 'neighborhood',
                  'phone_number']


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['username', 'first_name', 'last_name', 'password',
                  'created', 'email']


class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = ['creator', 'name', 'status', 'created', 'members']


class ValidatedCommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = ['id', 'creator', 'name', 'status', 'created', 'members']


class ComitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Comity
        fields = ['id', 'community', 'members']


class SaloonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Saloon
        fields = ['id', 'title', 'creator', 'community', 'supervisor', 'state', 'created']


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
        fields = ['creator', 'content', 'saloon']


class FirebaseMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'creator', 'content', 'saloon']
