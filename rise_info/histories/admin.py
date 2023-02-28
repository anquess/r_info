from django.contrib import admin

from .models import HistoryDB

class HistoryDBAdmin(admin.ModelAdmin):
    list_display = ('id', 'slug', 'update_at')

admin.site.register(HistoryDB, HistoryDBAdmin)
