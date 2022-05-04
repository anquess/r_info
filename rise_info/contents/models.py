from django.db import models

from rise_info.baseModels import CommonInfo, BaseAttachment


class Menu(models.Model):
    menu_title = models.CharField('タイトル', max_length=24)
    sort_num = models.IntegerField('並び順')

    def __str__(self):
        return self.menu_title

    class Meta:
        db_table = 'menus'


class Contents(CommonInfo):
    is_rich_text = models.BooleanField(
        verbose_name='リッチテキスト有効', default=False, help_text='内容のリッチテキスト有効/無効')
    menu = models.ForeignKey(Menu, verbose_name='menu',
                             on_delete=models.CASCADE, related_name='related_content')

    def save(self, *args, **kwargs):
        super(Contents, self).save(self, *args, **kwargs)

    class Meta:
        db_table = 'contents'


class AttachmentFile(BaseAttachment):
    info = models.ForeignKey(Contents, on_delete=models.CASCADE)
    upload_path = 'contents'

    class Meta:
        db_table = 'content_attachment'
