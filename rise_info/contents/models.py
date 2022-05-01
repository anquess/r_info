from django.db import models

from rise_info.baseModels import CommonInfo, BaseAttachment


class Contents(CommonInfo):
    is_rich_text = models.BooleanField(
        verbose_name='リッチテキスト有効', default=False, help_text='内容のリッチテキスト有効/無効')

    def save(self, *args, **kwargs):
        super(Contents, self).save(self, *args, **kwargs)

    class Meta:
        db_table = 'contents'


class Menu(models.Model):
    menu_title = models.CharField('タイトル', max_length=24)
    sort_num = models.IntegerField('並び順', unique=True)
    content = models.OneToOneField(
        Contents, verbose_name='コンテンツ', on_delete=models.CASCADE)

    class Meta:
        db_table = 'menus'


class AttachmentFile(BaseAttachment):
    info = models.ForeignKey(Contents, on_delete=models.CASCADE)
    upload_path = 'contents'

    class Meta:
        db_table = 'content_attachment'
