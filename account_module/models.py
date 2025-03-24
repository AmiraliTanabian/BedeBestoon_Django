from django.db import models
from django.contrib.auth.models import User

class TempUser(models.Model):
    username = models.CharField(max_length=255 ,verbose_name='نام کاربری')
    password = models.CharField(max_length=255 ,verbose_name='رمز عبور')
    email = models.EmailField(max_length=255 ,verbose_name='ایمیل')
    random_str = models.CharField(max_length=50 ,verbose_name='کد فعال‌سازی حساب')
    date = models.DateTimeField(verbose_name='تاریخ و زمان')


    def __str__(self):
        return f'{self.username}'

    class Meta:
        verbose_name = 'کاربر موقت'
        verbose_name_plural = 'کاربران موقت'

class ForgetPasswordUsers(models.Model):
    email = models.EmailField(max_length=255 ,verbose_name='ایمیل')
    random_str = models.CharField(max_length=50 ,verbose_name='کد فعال‌سازی حساب')

    class Meta:
        verbose_name = "کاربر درخواست تغییر رمز"
        verbose_name = "کاربران درخواست تغییر رمز"

class Token(models.Model):
    token = models.CharField(max_length=50, verbose_name='توکن')
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='کاربر')

    def __str__(self):
        return f'{self.user.username}_token'

    class Meta:
        verbose_name = 'توکن'
        verbose_name_plural = 'توکن ها'
