from django.contrib.auth import authenticate, login
from rest_framework import status, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, renderer_classes, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken, Token
from rest_framework_simplejwt.views import TokenObtainPairView
from knox.views import LoginView as KnoxLoginView

from recovering.serializers import *


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


"""class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        user = Member.objects.get(username=username)
        login(request, user)
        return super(LoginView, self).post(request, format=None)"""

class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super(MyObtainTokenPairView, self).post(request, *args, **kwargs)
        token = response.data['access']
        refresh = response.data['refresh']
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        member = authenticate(request, username=username, password=password)

        if member is not None:
            login(request, member)
        user = Member.objects.get(username=username)

        return Response(
            {'id': user.id, 'username': user.username, 'type': user.type, 'email': user.email, 'token': token})


"""class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        member = Member.objects.get(username=username)
        token, created = Token.objects.get_or_create(user=member)
        return Response({'member_id': member.id, 'token': token})"""


"""class LogoutView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response({"message": "User logged out successfully."})"""


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


@api_view(('GET',))
@renderer_classes((JSONRenderer,))
def community_integration(request, member_id, community_id):
    if request.method == 'GET':
        community = Community.objects.get(pk=community_id)
        member = Member.objects.get(pk=member_id)

        serializer = CommunitySerializer(community)

        community.members.add(member)

        return Response(serializer.data)


@api_view(('POST',))
@renderer_classes((JSONRenderer,))
@parser_classes([JSONParser])
def community_integration(request):
    if request.method == 'POST':
        community = Community.objects.get(pk=request.data["community_id"])
        member = Member.objects.get(pk=request.data["member_id"])

        serializer = CommunitySerializer(community)

        community.members.add(member)

        return Response(serializer.data)


@api_view(('POST',))
@parser_classes([JSONParser])
@renderer_classes((JSONRenderer,))
def community_pull_out(request):
    if request.method == 'POST':
        community = Community.objects.get(pk=request.data["community_id"])
        member = Member.objects.get(pk=request.data["member_id"])

        serializer = CommunitySerializer(community)

        community.members.remove(member)

        return Response(serializer.data)
