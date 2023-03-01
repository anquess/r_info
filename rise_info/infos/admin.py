from django.contrib import admin
from infos.models import Info, AttachmentFile, InfoComments, InfoRelation


class InfoRelationAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at',
                    'updated_by', 'updated_at')

class InfoAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at',
                    'updated_by', 'updated_at')

class InfoCommentsAdmin(admin.ModelAdmin):
    list_display = ('info', 'comment_txt', 'created_by')

class AttachmentFileAdmin(admin.ModelAdmin):
    list_display = ('info', 'filename')

admin.site.register(Info, InfoAdmin)
admin.site.register(InfoRelation, InfoRelationAdmin)
admin.site.register(InfoComments, InfoCommentsAdmin)
admin.site.register(AttachmentFile, AttachmentFileAdmin)
