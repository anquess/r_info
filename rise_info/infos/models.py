from django.db import models

from rise_info.baseModels import CommonInfo

class Info(CommonInfo):
    sammary = models.TextField(verbose_name='概要', default="", null=False, blank=True, max_length=512)

    def save(self, *args, **kwargs):
        super(Info, self).save(self, *args, **kwargs)
    
    class Meta:
        db_table = 'infos'