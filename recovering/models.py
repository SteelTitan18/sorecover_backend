from django.db import models
from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from datetime import *


# Create your models here.
class Member(User):
    phone_number = PhoneNumberField(verbose_name="Numéro de téléphone", unique=True)
    city = models.fields.charField(verbose_name="Ville", max_length=200)
    neighborhood = models.fields.charField(verbose_name="Quartier", max_length=200)


class PremiumMember(Member):

    def action(self):
        pass


class Supervisor(Member):

    def action(self):
        pass


class Admin(Member):

    def action(self):
        pass
