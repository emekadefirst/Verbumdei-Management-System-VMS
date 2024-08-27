# Generated by Django 5.1 on 2024-08-27 12:46

import parent.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=50)),
                ('phone_number_1', models.CharField(max_length=14)),
                ('phone_number_2', models.CharField(max_length=14)),
                ('parent_name', models.CharField(max_length=25)),
                ('home_address', models.CharField(max_length=150)),
                ('code', models.CharField(default=parent.models.parent_id, max_length=12, unique=True)),
            ],
        ),
    ]
