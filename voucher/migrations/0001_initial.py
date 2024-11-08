# Generated by Django 5.1.1 on 2024-11-08 00:21

import django.db.models.deletion
import voucher.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Voucher',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=55)),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('unit_cost', models.FloatField(blank=True, null=True)),
                ('code', models.CharField(default=voucher.models.voucher_code, max_length=20)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('DECLINED', 'Declined')], default='PENDING', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='voucher_type', to='inventory.inventorytype')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
