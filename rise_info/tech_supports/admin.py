from django.contrib import admin
from .models import TechSupports, AttachmentFile, TechSupportComments, TechSupportsRelation


class TechSupportsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at',
                    'updated_by', 'updated_at')


class TechSupportsRelationAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at',
                    'updated_by', 'updated_at')


admin.site.register(TechSupports, TechSupportsAdmin)
admin.site.register(TechSupportsRelation, TechSupportsRelationAdmin)
admin.site.register(AttachmentFile)
admin.site.register(TechSupportComments)
