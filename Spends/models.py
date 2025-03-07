from django.db import models
from django.contrib.auth.models import User

class Token(models.Model):
    token = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username}_token'

class Spend(models.Model):
    title = models.CharField(max_length=255)
    time = models.DateTimeField()
    price = models.BigIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} - {self.time.strftime("%Y-%m-%d | %H:%M")}'

class Income(models.Model):
    title = models.CharField(max_length=255)
    time = models.DateTimeField()
    price = models.BigIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} - {self.time.strftime("%Y-%m-%d | %H:%M")}'


class TempUser(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    random_str = models.CharField(max_length=50)
    date = models.DateTimeField()


    def __str__(self):
        return f'{self.username}'
