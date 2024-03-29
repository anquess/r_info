from django.db import models
from rise_info.baseModels import BaseManager

from datetime import datetime as dt
import pytz


class HistoryDB(models.Model):
    objects = BaseManager()
    slug = models.SlugField(verbose_name='対象データ', unique=True,
                            null=False, blank=False, max_length=20)
    update_at = models.DateTimeField(verbose_name='更新日時')

    def __str__(self):
        return self.slug

    class Meta:
        db_table = 'histories'
        verbose_name = 'インポート用履歴管理'
        verbose_name_plural = 'インポート用履歴管理'


def getLastUpdateAt(slug) -> dt:
    history = HistoryDB.objects.get_or_none(slug=slug)
    if history:
        last_update_at = history.update_at
        last_update_at = last_update_at.replace(
            tzinfo=pytz.timezone('Asia/Tokyo'))
    else:
        last_update_at = dt(2001, 1, 1, 0, 0, 0, 0,
                            tzinfo=pytz.timezone('Asia/Tokyo'))
    return last_update_at


def setLastUpdateAt(slug, last_update_at):
    history = HistoryDB.objects.get_or_none(slug=slug)
    if history:
        history.update_at = last_update_at
        history.save()
    else:
        HistoryDB.objects.create(slug=slug, update_at=last_update_at)
