# Generated by Django 5.1 on 2024-09-19 02:50

import django.db.models.deletion
import student.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('grade', '0001_initial'),
        ('parent', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('type', models.CharField(choices=[('DAY', 'day'), ('BOARDER', 'boarder')], max_length=20)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('registration_id', models.CharField(default=student.models.student_registration_id, max_length=20, unique=True)),
                ('first_name', models.CharField(max_length=25)),
                ('other_name', models.CharField(max_length=25)),
                ('last_name', models.CharField(max_length=25)),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(choices=[('MALE', 'male'), ('FEMALE', 'female')], max_length=20)),
                ('home_address', models.CharField(max_length=100)),
                ('state_of_origin', models.CharField(max_length=20)),
                ('local_government_area', models.CharField(max_length=20)),
                ('nationality', models.CharField(max_length=20)),
                ('religion', models.CharField(max_length=20)),
                ('upload', models.ImageField(blank=True, null=True, upload_to='Student_profile/')),
                ('img_url', models.URLField(blank=True, max_length=500)),
                ('registration_date', models.DateTimeField(auto_now=True)),
                ('class_assigned', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='grade.class')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parent.parent')),
            ],
            options={
                'ordering': ['-registration_date'],
            },
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('present', models.BooleanField(default=False)),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendances', to='grade.class')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendances', to='student.student')),
            ],
            options={
                'unique_together': {('student', 'grade', 'date')},
            },
        ),
    ]
