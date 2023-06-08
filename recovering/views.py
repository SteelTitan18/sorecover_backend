import pyrebase
from django.contrib.auth import authenticate, login
from django.db.models.signals import post_delete, pre_delete
from django.db.models import Q, QuerySet
from rest_framework import permissions
from rest_framework.decorators import api_view, renderer_classes, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny, BasePermission
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from recovering.serializers import *
from django.contrib.auth.decorators import permission_required
from rest_framework.views import APIView


# firebase connection
config = {
    "apiKey": "AIzaSyC6tx1tvItqzjh0GGBKQAZTIx83X78ta1k",

    "authDomain": "sorecover.firebaseapp.com",

    "databaseURL": "https://sorecover-default-rtdb.firebaseio.com",

    "projectId": "sorecover",

    "storageBucket": "sorecover.appspot.com",

    "messagingSenderId": "712261750260",

    "appId": "1:712261750260:web:1d4cc1ec2d93d5b79c3da1",

    "measurementId": "G-CKLF52DDH0"
}

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
db = firebase.database()


# Create your views here.
class IsCreatorOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.creator.username == request.user.username or request.user.is_staff


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST', 'GET']:
            return True
        elif request.method in ['PUT', 'DELETE']:
            return request.user and request.user.is_staff
        return False


class OnlyAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST']:
            print(request.user.is_staff)
            return request.user and request.user.is_staff
        return False

class MemberViewSet(ModelViewSet):
    serializer_class = MemberSerializer
    queryset = Member.objects.all()

    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        if 'community_id' in self.kwargs:
            community_id = self.kwargs['community_id']
            if community_id:
                return Community.objects.get(pk=community_id).members.all()
        else:
            return self.queryset

    def __str__(self):
        return self.username


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

        try:
            user = Member.objects.get(username=username)
            return Response(
                {'id': user.id, 'username': user.username, 'type': user.type, 'email': user.email, 'token': token,
                 'refresh': refresh})
        except:
            user = User.objects.get(username=username)
            return Response(
                {'id': user.id, 'username': user.username, 'email': user.email, 'token': token,
                 'refresh': refresh})


class VersionViewSet(ModelViewSet):
    serializer_class = VersionSerializer
    permission_classes = [IsCreatorOrAdmin]

    def get_queryset(self):
        return Version.objects.all()


class AdminViewSet(ModelViewSet):
    serializer_class = AdminSerializer

    # permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return Admin.objects.all()


class CommunityViewSet(ModelViewSet):
    # authentication_classes = [BasicAuthentication]
    permission_classes = [IsCreatorOrAdmin]
    serializer_class = CommunitySerializer

    def get_queryset(self):
        return Community.objects.all()


class ValidatedCommunityViewSet(ModelViewSet):
    permission_classes = [IsCreatorOrAdmin]
    serializer_class = ValidatedCommunitySerializer
    queryset = Community.objects.filter(status=Community.CommunityState.VALIDATED)

    def get_queryset(self):
        if 'member_id' in self.kwargs:
            member_id = [self.kwargs['member_id']]

            if member_id:
                return self.queryset.filter(Q(members__in=member_id))
            else:
                return self.queryset

        return self.queryset


class ComityViewSet(ModelViewSet):
    serializer_class = ComitySerializer
    permission_classes = [IsCreatorOrAdmin]

    def get_queryset(self):
        return Comity.objects.all()


class SaloonViewSet(ModelViewSet):
    serializer_class = SaloonSerializer
    permission_classes = [IsCreatorOrAdmin]

    queryset = Saloon.objects.all()

    def get_queryset(self):
        if 'community_id' in self.kwargs:
            community_id = self.kwargs['community_id']
            if community_id:
                return self.queryset.filter(community_id=community_id)
        elif 'member_id' in self.kwargs:
            member_id = [self.kwargs['member_id']]
            communities = Community.objects.filter(status=Community.CommunityState.VALIDATED)\
                .filter(Q(members__in=member_id))

            result = Saloon.objects.filter(title="")
            for community in communities.all():
                result = result | Saloon.objects.filter(community_id=community.id)
            return result

        else:
            return self.queryset


class CommunityValidationViewSet(ModelViewSet):
    serializer_class = CommunityValidationSerializer
    permission_classes = [IsCreatorOrAdmin]

    def get_queryset(self):
        return CommunityValidation.objects.all()


class FavoritesViewSet(ModelViewSet):
    serializer_class = FavoritesSerializer
    permission_classes = [IsCreatorOrAdmin]

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
    permission_classes = [IsCreatorOrAdmin]

    def get_queryset(self):
        return FinalVersion.objects.all()


"""class MessageViewSet(ModelViewSet):
    template_name = 'test.html'
    serializer_class = MessageSerializer
    queryset = Message.objects.all().order_by('created')
    permission_classes = [IsCreatorOrAdmin]

    def get_queryset(self):
        if 'saloon_id' in self.kwargs:
            saloon_id = self.kwargs['saloon_id']
            if saloon_id:
                return self.queryset.filter(saloon=saloon_id)
        else:
            return self.queryset"""



class ValidateCommunity(APIView):

    permission_classes = [IsAdminOrReadOnly]

    @renderer_classes((JSONRenderer,))
    @parser_classes([JSONParser])
    def post(self, request):
        community = Community.objects.get(pk=request.data["community_id"])
        community.status = community.CommunityState.VALIDATED

        serializer = CommunitySerializer(community)

        return Response(serializer.data)




class MessageViewSet(ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsCreatorOrAdmin]

    def get_queryset(self):
        queryset = Message.objects.all().order_by('created')

        saloon_id = self.kwargs['saloon_id']
        if saloon_id is not None:
            print("ok")
            saloon = Saloon.objects.get(pk=saloon_id)
            queryset = queryset.filter(saloon=saloon)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = self.queryset
        return context


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

        serializer = ValidatedCommunitySerializer(community)

        community.members.add(member)

        return Response(serializer.data)


@api_view(('POST',))
@parser_classes([JSONParser])
@renderer_classes((JSONRenderer,))
def community_pull_out(request):
    if request.method == 'POST':
        community = Community.objects.get(pk=request.data["community_id"])
        member = Member.objects.get(pk=request.data["member_id"])

        serializer = ValidatedCommunitySerializer(community)

        community.members.remove(member)

        return Response(serializer.data)


@api_view(('POST',))
@parser_classes([JSONParser])
@renderer_classes((JSONRenderer,))
def version_liking(request):
    if request.method == "POST":
        version = Version.objects.get(pk=request.data["version_id"])
        user = request.user

        serializer = VersionSerializer(version)

        if user in version.dislike.all():
            version.dislike.remove(user)
            version.like.add(user)
        elif user not in version.like.all():
            version.like.add(user)
        else:
            version.like.remove(user)

        return Response(serializer.data)


@api_view(('POST',))
@parser_classes([JSONParser])
@renderer_classes((JSONRenderer,))
def version_disliking(request):
    if request.method == "POST":
        version = Version.objects.get(pk=request.data["version_id"])
        user = request.user

        serializer = VersionSerializer(version)

        if user in version.like.all():
            version.like.remove(user)
            version.dislike.add(user)
        elif user not in version.dislike.all():
            version.dislike.add(user)
        else:
            version.dislike.remove(user)

        return Response(serializer.data)


@api_view(('POST',))
@parser_classes([JSONParser])
@renderer_classes((JSONRenderer,))
def message_taging(request):
    if request.method == "POST":
        message = Message.objects.get(pk=request.data["message_id"])
        tag = Message.objects.get(pk=request.data["tag_id"])

        serializer = MessageSerializer(message)

        if message != tag:
            message.message_tag = tag
            message.save()

        return Response(serializer.data)


@api_view(('POST',))
@parser_classes([JSONParser])
@renderer_classes((JSONRenderer,))
def version_taging(request):
    if request.method == "POST":
        message = Message.objects.get(pk=request.data["message_id"])
        tag = Version.objects.get(pk=request.data["tag_id"])

        serializer = MessageSerializer(message)

        message.version_tag = tag
        message.save()

        return Response(serializer.data)


"""@api_view(('POST',))
@renderer_classes((JSONRenderer,))
@parser_classes([JSONParser])
@permission_required([IsAdminOrReadOnly])
def validate_community(request):
    if request.method == 'POST':
        community = Community.objects.get(pk=request.data["community_id"])
        community.status = community.CommunityState.VALIDATED

        serializer = CommunitySerializer(community)

        return Response(serializer.data)"""


@api_view(('POST',))
@renderer_classes((JSONRenderer,))
@parser_classes([JSONParser])
@permission_required([OnlyAdmin])
def unvalidate_community(request):
    if request.method == 'POST':
        community = Community.objects.get(pk=request.data["community_id"])
        community.status = community.CommunityState.DRAFT

        serializer = CommunitySerializer(community)

        return Response(serializer.data)


@api_view(('POST',))
@renderer_classes((JSONRenderer,))
@parser_classes([JSONParser])
@permission_required([IsAdminOrReadOnly])
def get_usernames(request):
    if request.method == 'POST':
        usernames = {}
        id_list = request.data["id_list"]
        
        for id in id_list:
            usernames['{}'.format(id)] = Member.objects.get(pk=id).username

        return Response(usernames)


def firebase_messages_searching(message_id):
    messages = db.child('messages').get()
    for message in messages.each():
        if message.val()['id'] == message_id:
            return message
    return None


@receiver(post_save, sender=Message)
def firebase_save_update(sender, instance, **kwargs):
    data = FirebaseMessageSerializer(instance).data
    message = firebase_messages_searching(data['id'])
    if message:
        db.child("messages").child(message.key()).update(data)
    else:
        db.child("messages").push(data)


@receiver(pre_delete, sender=Message)
def firebase_delete_update(sender, instance, **kwargs):
    data = FirebaseMessageSerializer(instance).data
    message = firebase_messages_searching(data['id'])
    try:
        db.child("messages").child(message.key()).remove()
    except:
        pass
