from django.contrib import admin

from .models import FailuerReport, FailuerReportRelation, AttachmentFile, Circumstances
# SendedFailuerReport

admin.site.register(FailuerReport)
admin.site.register(FailuerReportRelation)
admin.site.register(AttachmentFile)
admin.site.register(Circumstances)
