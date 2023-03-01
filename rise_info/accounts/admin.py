from django.contrib import admin

from .models import User_mail_config

@admin.register(User_mail_config)
class UserMailConfigAdmin(admin.ModelAdmin):
    model = User_mail_config
    list_display = ('user', 'email_address')
