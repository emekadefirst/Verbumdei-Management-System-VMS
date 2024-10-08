# Generated by Django 5.1.1 on 2024-10-01 14:25

import Dormitary.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('staff', '0001_initial'),
        ('student', '0002_delete_attendance'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hostel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('MALE', 'Male'), ('FEMALE', 'Female')], max_length=20, unique=True)),
                ('warden', models.ForeignKey(limit_choices_to={'staff_type': 'NON_TEACHING'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='hostels', to='staff.staff')),
            ],
        ),
        migrations.CreateModel(
            name='Dorm',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('dorm_code', models.CharField(default=Dormitary.models.unique_room_id, max_length=10, unique=True)),
                ('max_occupants', models.PositiveIntegerField()),
                ('occupants', models.ManyToManyField(blank=True, to='student.student')),
                ('hostel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='Dormitary.hostel')),
            ],
        ),
    ]
