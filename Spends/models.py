from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Spend(models.Model):
    title = models.CharField(max_length=255, verbose_name='عنوان')
    time = models.DateTimeField(verbose_name='تاریخ و زمان')
    price = models.BigIntegerField(verbose_name='مبلغ')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    note = models.TextField(null=True, default="", verbose_name="یاداشت" , blank=True)


    def __str__(self):
        return f'{self.title} - {self.time.strftime("%Y-%m-%d | %H:%M")} - {self.price} هزار تومن'

    def get_absolute_url(self):
        return reverse("spend_detail", args=[self.id])

    class Meta:
        verbose_name = 'خرج'
        verbose_name_plural = 'مخارج'

class Income(models.Model):
    title = models.CharField(max_length=255 ,verbose_name='عنوان')
    time = models.DateTimeField(verbose_name='تاریخ و زمان')
    price = models.BigIntegerField(verbose_name='مبلغ')
    user = models.ForeignKey(User, on_delete=models.CASCADE ,verbose_name='کاربر')
    note = models.TextField(null=True, default="", verbose_name="یاداشت", blank=True)

    def __str__(self):
        return f'{self.title} - {self.time.strftime("%Y-%m-%d | %H:%M")} - {self.price} هزار تومن'


    def get_absolute_url(self):
        return reverse("income_detail", args=[self.id])

    class Meta:
        verbose_name = 'درآمد'
        verbose_name_plural = 'درآمد ها'
