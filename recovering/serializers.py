from rest_framework import serializers
from recovering.models import *


class VersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Version
        fields = ['id', 'title', 'author', 'audio', 'saloon', 'lyrics', 'created']


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id', 'username', 'type', 'first_name', 'last_name',
                  'created', 'email', 'city', 'neighborhood',
                  'phone_number']


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['id', 'first_name', 'last_name',
                  'created', 'email']


class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = ['id', 'creator', 'name', 'created']


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
