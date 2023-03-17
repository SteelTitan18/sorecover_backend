import threading
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField

current_user = threading.local()


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
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Community(models.Model):
    class CommunityState(models.TextChoices):
        DRAFT = 'DR', 'Draft'
        VALIDATED = 'VD', 'Validated'

    name = models.CharField(verbose_name="Nom: ", max_length=50, unique=True)
    status = models.CharField(verbose_name="Status", max_length=2, choices=CommunityState.choices,
                              default=CommunityState.DRAFT)
    creator = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='community_creator',
                                limit_choices_to={'type': Member.MemberType.PREMIUM})
    members = models.ManyToManyField(Member, related_name='community_members')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


@receiver(post_save, sender=Community)
def set_creator(sender, instance, **kwargs):
    instance.creator = Member.objects.get(pk=current_user.value.id)


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


@receiver(post_save, sender=Saloon)
def set_author(sender, instance, **kwargs):
    instance.author = Member.objects.get(pk=current_user.value.id)


class Version(models.Model):
    title = models.CharField(verbose_name='Titre: ', max_length=50)
    audio = models.FileField(upload_to='versions/audio/')
    author = models.ForeignKey(Member, related_name='project_version_author', on_delete=models.CASCADE)
    lyrics = models.FileField(upload_to='versions/lyrics/')
    created = models.DateTimeField(auto_now_add=True)
    saloon = models.ForeignKey(Saloon, related_name='version_saloon', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


@receiver(post_save, sender=Version)
def set_author(sender, instance, **kwargs):
    instance.author = Member.objects.get(pk=current_user.value.id)


class CommunityValidation(models.Model):
    validator = models.ForeignKey(Admin, related_name='validation_author', on_delete=models.DO_NOTHING)
    community = models.ForeignKey(Community, related_name='validation_community', on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.community.name


@receiver(pre_save, sender=Member)
def password_validation(sender, instance, **kwargs):
    original = Member.objects.get(pk=instance.pk)
    if instance.password != original.password:
        instance.set_password(instance.password)


@receiver(pre_save, sender=Admin)
def password_validation(sender, instance, **kwargs):
    original = Admin.objects.get(pk=instance.pk)
    if instance.password != original.password:
        instance.set_password(instance.password)


@receiver(post_save, sender=Community)
def create_comity(sender, instance, **kwargs):
    # Créer le comité directeur pour le nouveau groupe
    if not instance.pk:
        comity = Comity.objects.create(community=instance)
        comity.members.set([instance.creator.id])
        comity.save()


@receiver(pre_save, sender=Community)
def create_comity_validation(sender, instance, **kwargs):
    if instance.pk:
        # Si l'objet existe déjà, récupérez l'objet original depuis la base de données
        original = Community.objects.get(pk=instance.pk)
        # Si l'attribut 'status' a changé, créez un nouvel objet 'MyModel2'
        if (original.status != instance.status) and (original.status == Community.CommunityState.DRAFT):
            user = Admin.objects.get(pk=current_user.value.id)
            comity_validation = CommunityValidation.objects.create(community=instance,
                                                                   validator=user)
            # comity_validation.save()


class CurrentUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_user.value = request.user
        response = self.get_response(request)
        return response
