# Generated by Django 5.1.1 on 2024-09-30 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transport', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bus',
            name='year',
            field=models.CharField(max_length=5, null=True),
        ),
    ]