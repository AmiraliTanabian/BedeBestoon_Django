from django.contrib import admin
from .models import Spend, Income

class AdminSpendAndIncome(admin.ModelAdmin):
    list_display =  ['title', 'price', 'time', 'user']
    list_filter = ['time', 'user']

admin.site.register(Spend, AdminSpendAndIncome)
admin.site.register(Income, AdminSpendAndIncome)