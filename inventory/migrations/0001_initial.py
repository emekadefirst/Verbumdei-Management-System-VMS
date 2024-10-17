# Generated by Django 5.1.1 on 2024-10-17 10:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InventoryType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=55)),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('unit_cost', models.FloatField(blank=True, null=True)),
                ('time_of_purchase', models.DateTimeField(auto_now=True)),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='type', to='inventory.inventorytype')),
            ],
        ),
    ]
