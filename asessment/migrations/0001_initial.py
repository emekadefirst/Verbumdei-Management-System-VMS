# Generated by Django 5.1.1 on 2024-11-01 21:12

import asessment.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('EXAMINATION', 'Examination'), ('CONTINUOUS_ASSESSMENT', 'Continuous assessment')], max_length=25)),
                ('name', models.CharField(blank=True, max_length=55, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='QuizSession',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('code', models.CharField(default=asessment.models.exam_code, max_length=30, unique=True)),
                ('duration', models.IntegerField(blank=True, null=True)),
                ('status', models.CharField(choices=[('NOT STARTED', 'Not Started'), ('ONGOING', 'Ongoing'), ('ENDED', 'Ended')], default='NOT STARTED', max_length=20)),
            ],
            options={
                'ordering': ['-start_time'],
            },
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('correct', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('failed', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('total_questions', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('percentage', models.PositiveIntegerField(blank=True, default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='StudentResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200)),
                ('is_correct', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='asessment.question')),
            ],
        ),
    ]
