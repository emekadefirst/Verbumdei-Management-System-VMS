# Generated by Django 5.1 on 2024-09-20 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacheradmin', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacheradmin',
            name='token',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]