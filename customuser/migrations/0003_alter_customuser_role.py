# Generated by Django 5.1.1 on 2024-11-01 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customuser', '0002_alter_customuser_person_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('HEAD TEACHER', 'Head Teacher'), ('TEACHER', 'Teacher'), ('PARENT', 'Parent'), ('ACCOUNTANT', 'Accountant'), ('ADMIN', 'Admin'), ('MANAGER', 'Manager')], default='ADMIN', max_length=20),
        ),
    ]