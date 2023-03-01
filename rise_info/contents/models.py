from django.db import models
from django.db.models import Max

from addresses.models import Addresses
from rise_info.baseModels import CommonInfo, BaseAttachment, BaseManager, BaseCommnets


class Menu(models.Model):
    objects = BaseManager()
    menu_title = models.CharField('タイトル', max_length=24)
    sort_num = models.IntegerField(
        verbose_name='並び順', default=1, db_index=True)

    def __str__(self):
        return self.menu_title

    def create(self, *args, **kwargs):
        all_menu = Menu.objects.all()
        if all_menu.filter(sort_num=self.sort_num).count() > 0:
            max_val = all_menu.aggregate(Max('sort_num'))
            self.sort_num = max_val['sort_num__max'] + 1
        super(Menu, self).save(**kwargs)

    def save(self, *args, **kwargs):
        super(Menu, self).save(**kwargs)

    def replace_sort_num(self, subject: 'Menu', *args, **kwargs):
        if subject:
            self.sort_num, subject.sort_num = subject.sort_num, self.sort_num
            Menu.objects.bulk_update([self, subject], fields=['sort_num'])
        else:
            raise ValueError('対象が空です')

    class Meta:
        db_table = 'menus'
        verbose_name = 'メニュー'
        verbose_name_plural = 'メニュー一覧'

class Contents(CommonInfo):
    is_rich_text = models.BooleanField(
        verbose_name='リッチテキスト有効', default=False, help_text='内容のリッチテキスト有効/無効')
    addresses = models.ManyToManyField(
        Addresses, verbose_name='受信アドレス', null=True, blank=True,
        related_name='contents')

    def delete(self, *args, **kwargs):
        for attachment in self.attachmentfile_set.all():
            attachment.delete()
        return super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        return super().save(self, *args, **kwargs)

    class Meta:
        db_table = 'contents'
        verbose_name = '管技wikiコンテンツ(全データ)'
        verbose_name_plural = '管技wikiコンテンツ一覧(全データ)'

class AttachmentFile(BaseAttachment):
    info = models.ForeignKey(Contents, on_delete=models.CASCADE)
    upload_path = 'contents'

    class Meta:
        db_table = 'content_attachment'
        verbose_name = '管技wiki添付ファイル'
        verbose_name_plural = '管技wiki添付ファイル一覧'


class ContentComments(BaseCommnets):
   content = models.ForeignKey(
       Contents, related_name='contentComment', on_delete=models.CASCADE)
   upload_path = 'content_comments'
   class Meta:
       db_table = 'content_comments'
       verbose_name = '管技wikiコメント'
       verbose_name_plural = '管技wikiコメント一覧'

   def save(self, *args, **kwargs):
       if not self.pk:
           self.content.save()
       super(ContentComments, self).save(*args, **kwargs)


class ContentsRelation(Contents):
    send_info = models.OneToOneField(
        Contents, on_delete=models.DO_NOTHING, related_name='sended',
        verbose_name='送信ログ', null=True, blank=True)
    menu = models.ForeignKey(Menu, verbose_name='メニュー',
                             on_delete=models.CASCADE,
                             related_name='related_content')
    sort_num = models.IntegerField(
        verbose_name='並び順', default=1, db_index=True)

    def save(self, *args, **kwargs):
        self.sort_num = self.assign_sort_num()
        return super(Contents, self).save(self, *args, **kwargs)

    def replace_sort_num(self, subject: 'ContentsRelation', *args, **kwargs):
        if subject:
            self.sort_num, subject.sort_num = subject.sort_num, self.sort_num
            ContentsRelation.objects.bulk_update(
                [self, subject], fields=['sort_num'])
        else:
            raise ValueError('対象が空です')

    def assign_sort_num(self) -> int:
        content_querySet = ContentsRelation.objects.filter(
            menu=self.menu).all()
        if content_querySet.count() == 0:
            return self.sort_num
        if content_querySet.aggregate(Max('sort_num'))['sort_num__max'] + 1 < self.sort_num:
            return content_querySet.aggregate(Max('sort_num'))['sort_num__max'] + 1
        if content_querySet.filter(sort_num=self.sort_num).count() > 1:
            return content_querySet.aggregate(Max('sort_num'))['sort_num__max'] + 1
        if content_querySet.filter(sort_num=self.sort_num).count() == 1:
            if content_querySet.filter(sort_num=self.sort_num)[0].id != self.id:
                return content_querySet.aggregate(Max('sort_num'))['sort_num__max'] + 1
        return self.sort_num

    def delete(self, *args, **kwargs):
        if self.send_info:
            self.send_info.delete()
        return super().delete(*args, **kwargs)

    class Meta:
        db_table = 'contents_list'
        verbose_name = '管技wikiコンテンツ(一時保存のみ)'
        verbose_name_plural = '管技wikiコンテンツ一覧(一時保存のみ)'
