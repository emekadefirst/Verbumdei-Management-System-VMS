# Generated by Django 5.1.1 on 2024-10-27 23:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('grade', '0001_initial'),
        ('staff', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='teacher',
            field=models.OneToOneField(limit_choices_to={'staff_type': 'TEACHING'}, on_delete=django.db.models.deletion.CASCADE, to='staff.staff'),
        ),
        migrations.AddField(
            model_name='subject',
            name='grade',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subjects', to='grade.class'),
        ),
        migrations.AddField(
            model_name='subject',
            name='teacher',
            field=models.ForeignKey(limit_choices_to={'staff_type': 'TEACHING'}, on_delete=django.db.models.deletion.CASCADE, to='staff.staff'),
        ),
        migrations.AddField(
            model_name='subjectmaterial',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='study_materials', to='grade.subject'),
        ),
    ]
