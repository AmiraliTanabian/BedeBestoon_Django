from django.contrib import admin
from . import models
from django.contrib.auth.models import User

class AdminTempUser(admin.ModelAdmin):
    readonly_fields = ['random_str']
    list_display = ['__str__', 'date', 'email']
    list_filter = ['date']


class AdminSpendAndIncome(admin.ModelAdmin):
    list_display =  ['title', 'price', 'time', 'user']
    list_filter = ['time', 'user']


class AdminUser(admin.ModelAdmin):
    list_display = ['__str__', 'email', '']
admin.site.register(models.Income, AdminSpendAndIncome)
admin.site.register(models.Spend, AdminSpendAndIncome)
admin.site.register(models.Token)
admin.site.register(models.TempUser, AdminTempUser)