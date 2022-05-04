from re import sub
from django.db import models
from django.db.models import Max

from rise_info.baseModels import CommonInfo, BaseAttachment


class Menu(models.Model):
    menu_title = models.CharField('タイトル', max_length=24)
    sort_num = models.IntegerField(verbose_name='並び順', default=1)

    def __str__(self):
        return self.menu_title

    def save(self, *args, **kwargs):
        all_menu = Menu.objects.filter(sort_num=self.sort_num).all()
        if all_menu.count() > 0:
            max_val = all_menu.aggregate(Max('sort_num'))
            self.sort_num = max_val['sort_num__max'] + 1
        super(Menu, self).save(**kwargs)

    def replace_sort_num(self, subject: 'Menu', *args, **kwargs):
        if subject:
            self.sort_num, subject.sort_num = subject.sort_num, self.sort_num
            super(Menu, self).save(**kwargs)
            super(Menu, subject).save(**kwargs)
        else:
            raise ValueError('対象が空です')

    def save2(self, *args, **kwargs):
        super(Menu, self).save(**kwargs)

    class Meta:
        db_table = 'menus'


class Contents(CommonInfo):
    is_rich_text = models.BooleanField(
        verbose_name='リッチテキスト有効', default=False, help_text='内容のリッチテキスト有効/無効')
    menu = models.ForeignKey(Menu, verbose_name='メニュー',
                             on_delete=models.CASCADE, related_name='related_content')
    sort_num = models.IntegerField(verbose_name='並び順', default=1)

    def save(self, *args, **kwargs):
        content_querySet = Contents.objects.filter(
            menu=self.menu, sort_num=self.sort_num)
        if content_querySet.count() > 0:
            max_val = content_querySet.aggregate(Max('sort_num'))
            self.sort_num = max_val['sort_num__max'] + 1
        super(Contents, self).save(self, *args, **kwargs)

    def replace_sort_num(self, subject: 'Contents', *args, **kwargs):
        self.sort_num, subject.sort_num = subject.sort_num, self.sort_num
        super(Contents, subject).save(subject, *args, **kwargs)
        super(Contents, self).save(self, *args, **kwargs)

    class Meta:
        db_table = 'contents'


class AttachmentFile(BaseAttachment):
    info = models.ForeignKey(Contents, on_delete=models.CASCADE)
    upload_path = 'contents'

    class Meta:
        db_table = 'content_attachment'
