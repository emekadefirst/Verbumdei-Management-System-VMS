# Generated by Django 5.1.1 on 2024-10-19 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymenttype',
            name='payment_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='paymenttype',
            name='title',
            field=models.CharField(blank=True, max_length=1000, null=True, unique=True),
        ),
    ]
