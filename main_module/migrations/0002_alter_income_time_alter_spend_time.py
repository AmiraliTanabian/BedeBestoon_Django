# Generated by Django 5.1.4 on 2025-03-05 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_module', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='income',
            name='time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='spend',
            name='time',
            field=models.DateTimeField(),
        ),
    ]
