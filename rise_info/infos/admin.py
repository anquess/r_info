from django.contrib import admin
from infos.models import Info, AttachmentFile, InfoComments

admin.site.register(Info)
admin.site.register(InfoComments)
admin.site.register(AttachmentFile)
