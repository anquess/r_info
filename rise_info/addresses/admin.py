from django.contrib import admin
from .models import Addresses, RoleInLocal, InfoTypeRelationRole


class InfoTypeRelationRoleInline(admin.TabularInline):
    model = InfoTypeRelationRole


class RoleInLocalAdmin(admin.ModelAdmin):
    inlines = [
        InfoTypeRelationRoleInline,
    ]


admin.site.register(Addresses)
admin.site.register(RoleInLocal, RoleInLocalAdmin)

# Register your models here.
