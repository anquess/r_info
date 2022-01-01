from django.db import models

import os
import shutil

from rise_info.baseModels import CommonInfo, BaseManager

class Info(CommonInfo):
    sammary = models.TextField(verbose_name='概要', default="", null=False, blank=True, max_length=512)

    def save(self, *args, **kwargs):
        super(Info, self).save(self, *args, **kwargs)
    
    class Meta:
        db_table = 'infos'

def file_upload_path(instance, filename):
    return f"info/{str(instance.info.pk)}/{str(instance.pk)}/{filename}"

class InfoAttachment(models.Model):
    objects = BaseManager()
    info = models.ForeignKey(Info , on_delete=models.CASCADE)
    attachment = models.FileField(verbose_name='ファイル名', upload_to=file_upload_path)
    
    def save(self, *args, **kwargs):
        if self.id is None:
            upload_file = self.attachment
            self.attachment = None
            super().save(*args, **kwargs)
            self.attachment = upload_file
            if "force_insert" in kwargs:
                kwargs.pop("force_insert")
        elif os.path.isdir(f'uploads/info/{self.info.pk}/{self.id}'):
            shutil.rmtree(f'uploads/info/{self.info.pk}/{self.id}')
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'info_attachments'