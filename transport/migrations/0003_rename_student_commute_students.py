# Generated by Django 5.1.1 on 2024-09-30 08:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transport', '0002_alter_bus_year'),
    ]

    operations = [
        migrations.RenameField(
            model_name='commute',
            old_name='student',
            new_name='students',
        ),
    ]