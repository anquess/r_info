from django.conf import settings
from django.db import models
from django_currentuser.db.models import CurrentUserField
from django_currentuser.middleware import (get_current_user, get_current_authenticated_user)

from mdeditor.fields import MDTextField

class Info(models.Model):
    title = models.CharField(verbose_name='タイトル', default="", null=False, blank=False, max_length=128)
    sammary = models.TextField(verbose_name='概要', default="", null=False, blank=True, max_length=512)
    content = MDTextField(verbose_name='内容', default="", null=False, blank=True)
    created_by = CurrentUserField(verbose_name='登録者',on_update=True, related_name='create', null=False, blank=False)
    created_at = models.DateTimeField(verbose_name='投稿日', auto_now_add=True, null=False, blank=False)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True, null=False, blank=False)
    updated_by = CurrentUserField(verbose_name='更新者', on_update=True, related_name='update', null=False, blank=False)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_by = get_current_authenticated_user()
        self.updated_by = get_current_authenticated_user()
        super(Info, self).save(*args, **kwargs)
    
    class Meta:
        db_table = 'infos'