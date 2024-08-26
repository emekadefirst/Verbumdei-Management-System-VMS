# Generated by Django 5.1 on 2024-08-26 15:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('staff', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=12, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('teacher', models.OneToOneField(limit_choices_to={'staff_type': 'TEACHING'}, on_delete=django.db.models.deletion.CASCADE, to='staff.staff')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subjects', to='grade.class')),
                ('teacher', models.ForeignKey(limit_choices_to={'staff_type': 'TEACHING'}, on_delete=django.db.models.deletion.CASCADE, to='staff.staff')),
            ],
        ),
        migrations.CreateModel(
            name='SubjectMaterial',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('material', models.FileField(upload_to='study_materials/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='study_materials', to='grade.subject')),
            ],
        ),
    ]
