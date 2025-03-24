# Generated by Django 5.1.4 on 2025-03-24 03:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ForgetPasswordUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=255, verbose_name='ایمیل')),
                ('random_str', models.CharField(max_length=50, verbose_name='کد فعال\u200cسازی حساب')),
            ],
        ),
        migrations.CreateModel(
            name='TempUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255, verbose_name='نام کاربری')),
                ('password', models.CharField(max_length=255, verbose_name='رمز عبور')),
                ('email', models.EmailField(max_length=255, verbose_name='ایمیل')),
                ('random_str', models.CharField(max_length=50, verbose_name='کد فعال\u200cسازی حساب')),
                ('date', models.DateTimeField(verbose_name='تاریخ و زمان')),
            ],
            options={
                'verbose_name': 'کاربر موقت',
                'verbose_name_plural': 'کاربران موقت',
            },
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=50, verbose_name='توکن')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'توکن',
                'verbose_name_plural': 'توکن ها',
            },
        ),
    ]
