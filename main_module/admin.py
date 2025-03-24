from django.contrib import admin

class AdminSpendAndIncome(admin.ModelAdmin):
    list_display =  ['title', 'price', 'time', 'user']
    list_filter = ['time', 'user']
