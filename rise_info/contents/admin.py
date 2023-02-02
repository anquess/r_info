from django.contrib import admin

from contents.models import ContentsRelation, Menu, Contents, AttachmentFile, ContentComments


class ContentsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at',
                    'updated_by', 'updated_at')


class ContentsRelationAdmin(admin.ModelAdmin):
    list_display = ('title', 'menu', 'sort_num',
                    'updated_by', 'updated_at')


admin.site.register(Menu)
admin.site.register(Contents, ContentsAdmin)
admin.site.register(ContentsRelation, ContentsRelationAdmin)
admin.site.register(AttachmentFile)
admin.site.register(ContentComments)
