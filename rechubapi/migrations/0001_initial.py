# Generated by Django 3.1.7 on 2021-03-16 19:33

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'activity',
                'verbose_name_plural': 'activities',
            },
        ),
        migrations.CreateModel(
            name='Container',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name': 'container',
                'verbose_name_plural': 'containers',
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
            ],
            options={
                'verbose_name': 'status',
                'verbose_name_plural': 'statuses',
            },
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='rechubapi.activity')),
                ('container', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='rechubapi.container')),
            ],
            options={
                'verbose_name': 'trip',
                'verbose_name_plural': 'trips',
            },
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
            ],
            options={
                'verbose_name': 'type',
                'verbose_name_plural': 'types',
            },
        ),
        migrations.CreateModel(
            name='TripFriend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('friend', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rechubapi.trip')),
            ],
            options={
                'verbose_name': 'tripfriend',
                'verbose_name_plural': 'tripfriends',
            },
        ),
        migrations.CreateModel(
            name='TripContainer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('container', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rechubapi.container')),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rechubapi.trip')),
            ],
            options={
                'verbose_name': 'tripcontainer',
                'verbose_name_plural': 'tripcontainers',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('quantity', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='rechubapi.activity')),
                ('container', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='rechubapi.container')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='rechubapi.status')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='rechubapi.type')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'item',
                'verbose_name_plural': 'items',
            },
        ),
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('friend', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friends', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'friend',
                'verbose_name_plural': 'friends',
            },
        ),
    ]
