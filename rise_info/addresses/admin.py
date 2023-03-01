from django.contrib import admin
from .models import Addresses, RoleInLocal, InfoTypeRelationRole


class InfoTypeRelationRoleInline(admin.TabularInline):
    model = InfoTypeRelationRole
    

class RoleInLocalAdmin(admin.ModelAdmin):
    inlines = [
        InfoTypeRelationRoleInline,
    ]
    list_display = ('name', 'helpTXT')

@admin.register(Addresses)
class AddressesAdmin(admin.ModelAdmin):
    model = Addresses
    list_display = ('created_by', 'name', 'position', 'mail')

admin.site.register(RoleInLocal, RoleInLocalAdmin)

# Register your models here.
