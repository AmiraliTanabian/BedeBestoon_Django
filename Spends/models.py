from django.db import models
from django.contrib.auth.models import User

class Token(models.Model):
    token = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.first_name} --> {self.token}'

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


