from django.contrib import admin

from .models import FailuerReport, AttachmentFile, Circumstances
# SendedFailuerReport

admin.site.register(FailuerReport)
# admin.site.register(SendedFailuerReport)
admin.site.register(AttachmentFile)
admin.site.register(Circumstances)
