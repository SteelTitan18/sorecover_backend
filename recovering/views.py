from knox.models import AuthToken
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import *
from rest_framework import generics, permissions
from recovering.serializers import *
from recovering.models import *
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView


# Create your views here.
class MemberViewSet(ModelViewSet):
    serializer_class = MemberSerializer
    queryset = Member.objects.all()

    def get_queryset(self):
        if 'community_id' in self.kwargs:
            community_id = self.kwargs['community_id']
            if community_id:
                return Community.objects.get(pk=community_id).members
        else:
            return self.queryset


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


"""class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        member = serializer.save()

        return Response({
            "member": MemberSerializer(member, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(member)[1]
        })"""


class VersionViewSet(ModelViewSet):
    serializer_class = VersionSerializer

    def get_queryset(self):
        return Version.objects.all()


class AdminViewSet(ModelViewSet):
    serializer_class = AdminSerializer

    def get_queryset(self):
        return Admin.objects.all()


class CommunityViewSet(ModelViewSet):
    serializer_class = CommunitySerializer

    def get_queryset(self):
        return Community.objects.all()


class ValidatedCommunityViewSet(ModelViewSet):
    serializer_class = ValidatedCommunitySerializer

    def get_queryset(self):
        return Community.objects.filter(status=Community.CommunityState.VALIDATED)


class ComityViewSet(ModelViewSet):
    serializer_class = ComitySerializer

    def get_queryset(self):
        return Comity.objects.all()


class SaloonViewSet(ModelViewSet):
    serializer_class = SaloonSerializer
    queryset = Saloon.objects.all()

    def get_queryset(self):
        if 'community_id' in self.kwargs:
            community_id = self.kwargs['community_id']
            if community_id:
                return self.queryset.filter(community_id=community_id)
        else:
            return self.queryset


class CommunityValidationViewSet(ModelViewSet):
    serializer_class = CommunityValidationSerializer

    def get_queryset(self):
        return CommunityValidation.objects.all()

    """def members(self, request, pk=None, objs=None):
        community = Community.objects.get(pk=pk)
        members = community.members.all()
        page = self.paginate_queryset(members)
        if page is None:
            serializer = MemberSerializer(
                objs, context={'request': request}, many=True
            )
            return Response(serializer.data)
        else:
            serializer = MemberSerializer(
                page, context={'request': request}, many=True
            )
            return self.get_paginated_response(serializer.data)"""


class FavoritesViewSet(ModelViewSet):
    serializer_class = FavoritesSerializer

    def get_queryset(self):
        queryset = Favorites.objects.all()

        member_id = self.request.GET.get('member_id')
        if member_id is not None:
            request_member = Member.objects.get(pk=member_id)
            queryset = queryset.filter(member=request_member)

        version_id = self.request.GET.get('version_id')
        if version_id is not None:
            request_version = Version.objects.get(pk=version_id)
            queryset = queryset.filter(version=request_version)

        return queryset


class FinalVersionViewSet(ModelViewSet):
    serializer_class = FinalVersionSerializer

    def get_queryset(self):
        return FinalVersion.objects.all()


class MessageViewSet(ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all().order_by('created')

    def get_queryset(self):
        if 'saloon_id' in self.kwargs:
            saloon_id = self.kwargs['saloon_id']
            if saloon_id:
                return self.queryset.filter(saloon=saloon_id)
        else:
            return self.queryset


"""class CommunityMembers(ModelViewSet):
    serializer_class = MemberSerializer

    def get_queryset(self):
        return Member.objects.filter(c)
"""
