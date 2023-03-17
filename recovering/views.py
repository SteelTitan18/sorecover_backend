from rest_framework.viewsets import ModelViewSet
from recovering.serializers import *
from recovering.models import *


# Create your views here.
class MemberViewSet(ModelViewSet):
    serializer_class = MemberSerializer

    def get_queryset(self):
        return Member.objects.all()


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

    def get_queryset(self):
        return Saloon.objects.all()


class CommunityValidationViewSet(ModelViewSet):
    serializer_class = CommunityValidationSerializer

    def get_queryset(self):
        return CommunityValidation.objects.all()
