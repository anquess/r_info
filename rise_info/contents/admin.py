from django.contrib import admin

from contents.models import Menu, Contents, AttachmentFile, ContentComments

admin.site.register(Menu)
admin.site.register(Contents)
admin.site.register(AttachmentFile)
admin.site.register(ContentComments)
# Register your models here.
