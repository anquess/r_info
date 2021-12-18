from django.contrib import admin
from infos.models import Info

from markdownx.admin import MarkdownxModelAdmin

admin.site.register(Info, MarkdownxModelAdmin)