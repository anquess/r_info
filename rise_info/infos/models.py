from django.db import models

import os
import shutil

from rise_info.baseModels import CommonInfo, BaseManager, Attachment, file_upload_path

class Info(CommonInfo):
    sammary = models.TextField(verbose_name='概要', default="", null=False, blank=True, max_length=512)

    def save(self, *args, **kwargs):
        super(Info, self).save(self, *args, **kwargs)
    
    class Meta:
        db_table = 'infos'

#def file_upload_path(instance, filename):
#    return f"info/{str(instance.info.pk)}/{str(instance.pk)}/{filename}"

class InfoAttachmentFile(Attachment):
    info = models.ForeignKey(Info , on_delete=models.CASCADE)
    upload_path = 'info'
    class Meta:
        db_table = 'info_attachments'