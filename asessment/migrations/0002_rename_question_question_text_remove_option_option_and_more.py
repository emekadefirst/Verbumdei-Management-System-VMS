# Generated by Django 5.1.1 on 2024-10-31 04:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asessment', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='question',
            new_name='text',
        ),
        migrations.RemoveField(
            model_name='option',
            name='option',
        ),
        migrations.RemoveField(
            model_name='question',
            name='options',
        ),
        migrations.AddField(
            model_name='option',
            name='question',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='options', to='asessment.question'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='option',
            name='text',
            field=models.CharField(default=None, max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='option',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='question',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='question',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='asessment.quiz'),
        ),
    ]