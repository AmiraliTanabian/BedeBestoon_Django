from django.contrib import admin
from . import models

class AdminTempUser(admin.ModelAdmin):
    readonly_fields = ['random_str']
    list_display = ['__str__', 'date', 'email']
    list_filter = ['date']

class AdminUser(admin.ModelAdmin):
    list_display = ['__str__', 'email', '']

admin.site.register(models.Token)
admin.site.register(models.TempUser, AdminTempUser)