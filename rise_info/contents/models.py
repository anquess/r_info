from django.db import models
from django.db.models import Max

from rise_info.baseModels import CommonInfo, BaseAttachment, BaseManager


class Menu(models.Model):
    objects = BaseManager()
    menu_title = models.CharField('タイトル', max_length=24)
    sort_num = models.IntegerField(
        verbose_name='並び順', default=1, db_index=True)

    def __str__(self):
        return self.menu_title

    def save(self, *args, **kwargs):
        all_menu = Menu.objects.all()
        if all_menu.filter(sort_num=self.sort_num).count() > 0:
            max_val = all_menu.aggregate(Max('sort_num'))
            self.sort_num = max_val['sort_num__max'] + 1
        super(Menu, self).save(**kwargs)

    def replace_sort_num(self, subject: 'Menu', *args, **kwargs):
        if subject:
            self.sort_num, subject.sort_num = subject.sort_num, self.sort_num
            Menu.objects.bulk_update([self, subject], fields=['sort_num'])
        else:
            raise ValueError('対象が空です')

    class Meta:
        db_table = 'menus'


class Contents(CommonInfo):
    is_rich_text = models.BooleanField(
        verbose_name='リッチテキスト有効', default=False, help_text='内容のリッチテキスト有効/無効')
    menu = models.ForeignKey(Menu, verbose_name='メニュー',
                             on_delete=models.CASCADE, related_name='related_content')
    sort_num = models.IntegerField(
        verbose_name='並び順', default=1, db_index=True)

    def save(self, *args, **kwargs):
        self.sort_num = self.assign_sort_num()
        super(Contents, self).save(self, *args, **kwargs)

    def replace_sort_num(self, subject: 'Contents', *args, **kwargs):
        if subject:
            self.sort_num, subject.sort_num = subject.sort_num, self.sort_num
            Contents.objects.bulk_update([self, subject], fields=['sort_num'])
        else:
            raise ValueError('対象が空です')

    def assign_sort_num(self) -> int:
        content_querySet = Contents.objects.filter(menu=self.menu).all()
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

    class Meta:
        db_table = 'contents'


class AttachmentFile(BaseAttachment):
    info = models.ForeignKey(Contents, on_delete=models.CASCADE)
    upload_path = 'contents'

    class Meta:
        db_table = 'content_attachment'
