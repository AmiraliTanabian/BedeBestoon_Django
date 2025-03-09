from django.db import models

class Messages(models.Model):
    name = models.CharField(max_length=255, verbose_name="نام ارسال کننده")
    subject = models.CharField(max_length=255, verbose_name="موضوع پیام")
    email = models.EmailField(verbose_name="ایمیل ارسال کننده")
    text = models.TextField(verbose_name="متن پیام")
    datetime = models.DateTimeField(verbose_name='زمان ارسال پیام')

    def __str__(self):
        return f'{self.name} - {self.subject}'

    class Meta:
        verbose_name="پیام"
        verbose_name_plural = "پیام ها"