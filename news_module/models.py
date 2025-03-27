from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class NewsModel(models.Model):
    writer = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="نویسنده")
    title = models.CharField(max_length=100, verbose_name="تیتر خبر")
    banner = models.ImageField(upload_to="NewsBanner/", verbose_name="تصویر اصلی")
    slug = models.SlugField(db_index=True, verbose_name="اسلاگ", blank=True, allow_unicode=True)
    text = models.TextField()
    datetime = models.DateField(verbose_name="آخرین ویرایش"),
    short_info = models.CharField(max_length=255,default="", verbose_name="توضیحات کوتاه")
    is_active = models.BooleanField(default=True, verbose_name="فعال بودن خبر")


    def __str__(self):
        return f"{self.title} - {self.writer}"

    class Meta:
        verbose_name= "خبر"
        verbose_name_plural = "اخبار"


    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)