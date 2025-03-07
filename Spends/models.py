from django.db import models
from django.contrib.auth.models import User

class Token(models.Model):
    token = models.CharField(max_length=50, verbose_name='توکن')
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='کاربر')

    def __str__(self):
        return f'{self.user.username}_token'

    class Meta:
        verbose_name = 'توکن'
        verbose_name_plural = 'توکن ها'

class Spend(models.Model):
    title = models.CharField(max_length=255, verbose_name='عنوان')
    time = models.DateTimeField(verbose_name='تاریخ و زمان')
    price = models.BigIntegerField(verbose_name='مبلغ')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')

    def __str__(self):
        return f'{self.title} - {self.time.strftime("%Y-%m-%d | %H:%M")} - {self.price} هزار تومن'

    class Meta:
        verbose_name = 'خرج'
        verbose_name_plural = 'مخارج'

class Income(models.Model):
    title = models.CharField(max_length=255 ,verbose_name='عنوان')
    time = models.DateTimeField(verbose_name='تاریخ و زمان')
    price = models.BigIntegerField(verbose_name='مبلغ')
    user = models.ForeignKey(User, on_delete=models.CASCADE ,verbose_name='کاربر')

    def __str__(self):
        return f'{self.title} - {self.time.strftime("%Y-%m-%d | %H:%M")} - {self.price} هزار تومن'

    class Meta:
        verbose_name = 'درآمد'
        verbose_name_plural = 'درآمد ها'

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