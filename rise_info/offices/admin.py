from django.contrib import admin
from .models import Office, OfficesGroup

class OfficesAdmin(admin.ModelAdmin):
    list_display = ('id', 'unyo_sts', 'name', 'shortcut_name')

admin.site.register(Office, OfficesAdmin)
admin.site.register(OfficesGroup)
