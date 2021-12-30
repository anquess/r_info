from django.db import models

import os

from rise_info.baseModels import CommonInfo, BaseManager

class Info(CommonInfo):
    sammary = models.TextField(verbose_name='概要', default="", null=False, blank=True, max_length=512)

    def save(self, *args, **kwargs):
        super(Info, self).save(self, *args, **kwargs)
    
    class Meta:
        db_table = 'infos'

class InfoAttachment(models.Model):
    objects = BaseManager()
    info = models.ForeignKey(Info , on_delete=models.CASCADE)
    file = models.FileField(verbose_name='ファイル名', default='', null=False, blank=True, max_length=64)

    class Meta:
        db_table = 'info_attachments'