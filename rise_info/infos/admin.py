from django.contrib import admin
from infos.models import Info, AttachmentFile, InfoComments, InfoRelation


class InfoRelationAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at',
                    'updated_by', 'updated_at')


class InfoAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at',
                    'updated_by', 'updated_at')


admin.site.register(Info, InfoAdmin)
admin.site.register(InfoRelation, InfoRelationAdmin)
admin.site.register(InfoComments)
admin.site.register(AttachmentFile)
