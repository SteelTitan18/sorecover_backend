from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


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
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Admin(User):

    def __str__(self):
        return self.username


class Community(models.Model):
    name = models.CharField(verbose_name="Nom: ", max_length=50, unique=True)
    members = models.ManyToManyField(Member, related_name='community_members')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Comity(models.Model):
    community = models.OneToOneField(Community, on_delete=models.CASCADE)
    members = models.ManyToManyField(Member, related_name='comity_members')

    def __str__(self):
        return self.community.name


class Saloon(models.Model):
    class SaloonState(models.TextChoices):
        BEGINNING = 'BG', 'Beginning'
        PROGRESSING = 'PR', 'Progressing'
        FINISH = 'FN', 'Finish'

    title = models.CharField(max_length=100, verbose_name='title')
    author = models.ForeignKey(Member, related_name='version_author', on_delete=models.CASCADE)
    supervisor = models.ForeignKey(Member, related_name='saloon_supervisor',
                                   on_delete=models.CASCADE,
                                   limit_choices_to={'type': Member.MemberType.SUPERVISOR})
    members = models.ManyToManyField(Member, related_name='saloon_members')
    state = models.CharField(max_length=2, choices=SaloonState.choices, default=SaloonState.BEGINNING)
    created = models.DateTimeField(auto_now_add=True)
    community = models.ForeignKey(Community, related_name='saloon_community', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Version(models.Model):
    title = models.CharField(verbose_name='Titre: ', max_length=50)
    audio = models.FileField(upload_to='versions/audio/')
    author = models.ForeignKey(Member, related_name='project_version_author', on_delete=models.CASCADE)
    lyrics = models.FileField(upload_to='versions/lyrics/')
    created = models.DateTimeField(auto_now_add=True)
    saloon = models.ForeignKey(Saloon, related_name='version_saloon', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
