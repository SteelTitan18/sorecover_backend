from django.db import models
from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from datetime import *


# Create your models here.
class Member(User):
    class MemberType(models.TextChoices):
        SIMPLE = 'SP', 'Simple'
        PREMIUM = 'PM', 'Premium'
        SUPERVISOR = 'SV', 'Supervisor'

    phone_number = PhoneNumberField(verbose_name="Numéro de téléphone", unique=True)
    city = models.fields.CharField(verbose_name="Ville", max_length=200)
    neighborhood = models.fields.CharField(verbose_name="Quartier", max_length=200)
    type = models.CharField(verbose_name="Type d'utilisateur", max_length=2, choices=MemberType.choices,
                            default=MemberType.SIMPLE)


class Admin(User):

    def validate_creation(self):
        pass


class Community(models.Model):
    name = models.CharField(verbose_name="Nom: ", max_length=50, unique=True)
    members = models.ManyToManyField(Member, related_name='community_members')
    admins = models.ManyToManyField(Admin, related_name='community_admins')
    created = models.DateTimeField(auto_now_add=True)


class Comity(models.Model):
    members = models.ManyToManyField(Member, related_name='comity_members')


class Version(models.Model):
    title = models.CharField(verbose_name='Titre: ', max_length=50)
    audio = models.FileField(upload_to='versions/audio/')
    author = models.ForeignKey(Member, related_name='project_version_author', on_delete=models.CASCADE)
    lyrics = models.FileField(upload_to='versions/lyrics/')
    created = models.DateTimeField(auto_now_add=True)


class Saloon(models.Model):
    class SaloonState(models.TextChoices):
        BEGINNING = 'BG', 'Beginning'
        PROGRESSING = 'PR', 'Progressing'
        FINISH = 'FN', 'Finish'

    author = models.ForeignKey(Member, related_name='version_author', on_delete=models.CASCADE)
    supervisor = models.ForeignKey(Member, related_name='saloon_supervisor',
                                   on_delete=models.CASCADE,
                                   limit_choices_to={Member.type == Member.MemberType.SUPERVISOR})
    versions = models.ManyToManyField(Version, related_name='saloon_versions')
    members = models.ManyToManyField(Member, related_name='saloon_members')
    state = models.CharField(max_length=2, choices=SaloonState.choices, default=SaloonState.BEGINNING)
