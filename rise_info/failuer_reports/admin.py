from django.contrib import admin

from .models import FailuerReport, FailuerReportRelation, AttachmentFile, Circumstances
# SendedFailuerReport

class FailuerReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'select_register', 'created_by', 'failuer_date')

class AttachmentFileAdmin(admin.ModelAdmin):
    list_display = ('info', 'filename')

class CircumstancesAdmin(admin.ModelAdmin):
    list_display = ('info', 'event')

admin.site.register(FailuerReport, FailuerReportAdmin)
admin.site.register(FailuerReportRelation, FailuerReportAdmin)
admin.site.register(AttachmentFile, AttachmentFileAdmin)
admin.site.register(Circumstances, CircumstancesAdmin)
