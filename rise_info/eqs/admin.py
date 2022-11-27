from django.contrib import admin

from .models import Eqtype, DepartmentForEq


class DepartmentForEqAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    fields = ['id', 'name']


class EqtypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'slug']
    fields = ['department']
    readonly_fields = ['id', 'slug']


# Register your models here.
admin.site.register(Eqtype, EqtypeAdmin)
admin.site.register(DepartmentForEq, DepartmentForEqAdmin)
