from django.contrib import admin
from .models import TechSupports, AttachmentFile, TechSupportComments, TechSupportsRelation


class TechSupportsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at',
                    'updated_by', 'updated_at')

class TechSupportsRelationAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at',
                    'updated_by', 'updated_at')

class AttachmentFileAdmin(admin.ModelAdmin):
    list_display = ('info', 'filename')

class TechSupportCommentsAdmin(admin.ModelAdmin):
    list_display = ('info', 'comment_txt', 'created_by')

admin.site.register(TechSupports, TechSupportsAdmin)
admin.site.register(TechSupportsRelation, TechSupportsRelationAdmin)
admin.site.register(AttachmentFile, AttachmentFileAdmin)
admin.site.register(TechSupportComments, TechSupportCommentsAdmin)
