# Generated by Django 4.1.7 on 2023-03-16 02:05

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Community',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Nom: ')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True, verbose_name='Numéro de téléphone')),
                ('city', models.CharField(max_length=200, verbose_name='Ville')),
                ('neighborhood', models.CharField(max_length=200, verbose_name='Quartier')),
                ('type', models.CharField(choices=[('SP', 'Simple'), ('PM', 'Premium'), ('SV', 'Supervisor')], default='SP', max_length=2, verbose_name="Type d'utilisateur")),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Saloon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('state', models.CharField(choices=[('BG', 'Beginning'), ('PR', 'Progressing'), ('FN', 'Finish')], default='BG', max_length=2)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='version_author', to='recovering.member')),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saloon_community', to='recovering.community')),
                ('members', models.ManyToManyField(related_name='saloon_members', to='recovering.member')),
                ('supervisor', models.ForeignKey(limit_choices_to={'type': 'SV'}, on_delete=django.db.models.deletion.CASCADE, related_name='saloon_supervisor', to='recovering.member')),
            ],
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Titre: ')),
                ('audio', models.FileField(upload_to='versions/audio/')),
                ('lyrics', models.FileField(upload_to='versions/lyrics/')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_version_author', to='recovering.member')),
                ('saloon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='version_saloon', to='recovering.saloon')),
            ],
        ),
        migrations.AddField(
            model_name='community',
            name='members',
            field=models.ManyToManyField(related_name='community_members', to='recovering.member'),
        ),
        migrations.CreateModel(
            name='Comity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('community', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='recovering.community')),
                ('members', models.ManyToManyField(related_name='comity_members', to='recovering.member')),
            ],
        ),
    ]
