# Generated by Django 5.1.4 on 2025-03-24 03:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_module', '0009_forgetpasswordusers'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ForgetPasswordUsers',
        ),
        migrations.DeleteModel(
            name='TempUser',
        ),
        migrations.DeleteModel(
            name='Token',
        ),
    ]
