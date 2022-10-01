from django.contrib import admin
from .models import FailuerReport, AttachmentFile, Circumstances

admin.site.register(FailuerReport)
admin.site.register(AttachmentFile)
admin.site.register(Circumstances)
