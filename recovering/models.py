import threading

from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from phonenumber_field.modelfields import PhoneNumberField

from sorecover import settings

current_user = threading.local()


# Create your models here.
class Member(User):
    class MemberType(models.TextChoices):
        SIMPLE = 'SP', 'Simple'
        PREMIUM = 'PM', 'Premium'

    phone_number = PhoneNumberField(verbose_name="Numéro de téléphone", unique=True)
    city = models.fields.TextField(verbose_name="Ville", max_length=200)
    neighborhood = models.fields.TextField(verbose_name="Quartier", max_length=200, blank=True, null=True)
    type = models.CharField(verbose_name="Type d'utilisateur", max_length=2, choices=MemberType.choices,
                            default=MemberType.SIMPLE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Admin(User):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_staff = True

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
    image = models.FileField(upload_to='communities/images/', blank=True, null=True)
    creator = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='community_creator',
                                limit_choices_to={'type': Member.MemberType.PREMIUM})
    description = models.TextField(verbose_name="Description", max_length=300)
    members = models.ManyToManyField(Member, related_name='community_members', blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


@receiver(post_save, sender=Community)
def add_first_member(sender, instance, **kwargs):
    member = Member.objects.get(pk=instance.creator)
    if member not in instance.members.all():
        print("ok")
        instance.members.add(Member.objects.get(pk=instance.creator))


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
    description = models.TextField(verbose_name="Description", max_length=300)
    creator = models.ForeignKey(Member, related_name='version_creator', on_delete=models.CASCADE)
    supervisor = models.ForeignKey(Member, related_name='saloon_supervisor',
                                   on_delete=models.CASCADE)
    state = models.CharField(max_length=2, choices=SaloonState.choices, default=SaloonState.BEGINNING)
    created = models.DateTimeField(auto_now_add=True)
    community = models.ForeignKey(Community, related_name='saloon_community', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


@receiver(post_save, sender=Saloon)
def set_creator(sender, instance, **kwargs):
    if not instance.pk:
        instance.creator = Member.objects.get(pk=current_user.value.id)


class Version(models.Model):
    title = models.CharField(verbose_name='Titre: ', max_length=50)
    audio = models.FileField(upload_to='versions/audio/')
    creator = models.ForeignKey(Member, related_name='project_version_creator', on_delete=models.CASCADE)
    lyrics = models.FileField(upload_to='versions/lyrics/', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    saloon = models.ForeignKey(Saloon, related_name='version_saloon', on_delete=models.CASCADE)
    like = models.ManyToManyField(User, related_name="likers", blank=True, null=True)
    dislike = models.ManyToManyField(User, related_name="dislikers", blank=True, null=True)

    def __str__(self):
        return self.title


@receiver(post_save, sender=Version)
def set_saloon_status(sender, instance, **kwargs):
    instance.saloon.state = Saloon.SaloonState.PROGRESSING
    instance.saloon.save()


class Favorites(models.Model):
    member = models.ForeignKey(Member, related_name='favorite_creator', on_delete=models.CASCADE)
    version = models.ForeignKey(Version, related_name='favorite_version', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.version.title


class CommunityValidation(models.Model):
    validator = models.ForeignKey(Admin, related_name='validation_creator', on_delete=models.DO_NOTHING)
    community = models.ForeignKey(Community, related_name='validation_community', on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.community.name


class Message(models.Model):
    creator = models.ForeignKey(Member, related_name='message_creator', on_delete=models.CASCADE)
    content = models.CharField(verbose_name="contenu", max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    saloon = models.ForeignKey(Saloon, related_name='message_saloon', on_delete=models.CASCADE)
    message_tag = models.ForeignKey('self', related_name='tag_on_message', on_delete=models.DO_NOTHING, null=True,
                                    blank=True)
    version_tag = models.ForeignKey(Version, related_name='tag_on_version', on_delete=models.DO_NOTHING, null=True,
                                    blank=True)

    def __str__(self):
        return self.content


class FinalVersion(models.Model):
    version = models.ForeignKey(Version, related_name='validated_version', on_delete=models.CASCADE)
    saloon = models.ForeignKey(Saloon, related_name='terminate_saloon', on_delete=models.CASCADE)

    def __str__(self):
        return self.saloon.title


@receiver(pre_save, sender=FinalVersion)
def set_saloon(sender, instance, **kwargs):
    instance.saloon = instance.version.saloon
    # instance.save()


@receiver(post_save, sender=FinalVersion)
def terminate_saloon(sender, instance, **kwargs):
    instance.saloon.state = Saloon.SaloonState.FINISH
    instance.saloon.save()


@receiver(pre_save, sender=Member)
def password_validation(sender, instance, **kwargs):
    if not instance.pk:
        instance.set_password(instance.password)
    else:
        original = Member.objects.get(pk=instance.pk)
        if instance.password != original.password:
            instance.set_password(instance.password)


@receiver(pre_save, sender=Admin)
def password_validation(sender, instance, **kwargs):
    if not instance.pk:
        instance.set_password(instance.password)
    else:
        original = Admin.objects.get(pk=instance.pk)
        if instance.password != original.password:
            instance.set_password(instance.password)


@receiver(post_save, sender=Community)
def create_comity(sender, instance, **kwargs):
    try:
        verification = Comity.objects.get(community=instance)
    except:
        comity = Comity.objects.create(community=instance)
        comity.members.set([instance.creator.id])
        comity.save()


@receiver(pre_save, sender=Community)
def create_community_validation(sender, instance, **kwargs):
    try:
        user = Admin.objects.get(pk=current_user.value.id)
        if instance.pk:
            original = Community.objects.get(pk=instance.pk)
            if (original.status != instance.status) and (original.status == Community.CommunityState.DRAFT):
                CommunityValidation.objects.create(community=instance, validator=user)
    except:
        pass


class CurrentUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_user.value = request.user
        response = self.get_response(request)
        return response


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    email_plaintext_message = "http://127.0.0.1:8000{}?token={}".format(
        reverse('password_reset:reset-password-request'),
        reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        "Copiez ce code : ".format(
            reset_password_token.key),
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [reset_password_token.user.email]
    )
