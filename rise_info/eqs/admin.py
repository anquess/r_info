from django.contrib import admin

from .models import Eqtype, DepartmentForEq, EQ_class


class DepartmentForEqAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    fields = ['id', 'name']


class EqtypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'slug']
    fields = ['department', 'id', 'slug']
    readonly_fields = ['id', 'slug']


# Register your models here.
admin.site.register(Eqtype, EqtypeAdmin)
admin.site.register(DepartmentForEq, DepartmentForEqAdmin)
admin.site.register(EQ_class)
