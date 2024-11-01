# Generated by Django 5.1.1 on 2024-11-01 21:12

import Dormitary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hostel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('MALE', 'Male'), ('FEMALE', 'Female')], max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Dorm',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('dorm_code', models.CharField(default=Dormitary.models.unique_room_id, max_length=10, unique=True)),
                ('max_occupants', models.PositiveIntegerField()),
                ('occupants', models.ManyToManyField(blank=True, to='student.student')),
            ],
        ),
    ]
