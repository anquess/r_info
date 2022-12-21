from django.contrib.auth.models import Group
from django.db import models
from django_currentuser.db.models import CurrentUserField
from django_currentuser.middleware import (get_current_authenticated_user)


from rise_info.baseModels import BaseManager
from eqs.models import DepartmentForEq
from offices.models import Office, OfficesGroup

# Create your models here.


class Addresses(models.Model):
    object = BaseManager()
    name = models.CharField(verbose_name='氏名', null=False,
                            blank=False, max_length=16)
    position = models.CharField(
        verbose_name='役職', null=False, blank=False, max_length=16)
    mail = models.EmailField(verbose_name='メールアドレス', null=False, blank=False)
    groups = models.ManyToManyField(
        Group,
        verbose_name='障害通報書配信元官署グループ', related_name='addresses', blank=True,
        help_text='障害通報書の配信元官署グループ(Ctrlにより複数選択可能)'
    )
    department = models.ManyToManyField(
        DepartmentForEq,
        verbose_name='担当装置分類', related_name='addresses', blank=True,
        help_text='障害通報で登録した官署のタグが1つでもあれば宛先として表示されます'
    )
    created_by = CurrentUserField(
        verbose_name='登録者', on_update=True,
        related_name='%(app_label)s_%(class)s_create', null=False, blank=False
    )

    def __str__(self):
        return self.position + ' ' + self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_by = get_current_authenticated_user()
        super(Addresses, self).save(*args, **kwargs)

    class Meta:
        db_table = 'addresses'
