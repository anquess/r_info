from django.contrib.auth.models import Group
from django.db import models
from django_currentuser.db.models import CurrentUserField
from django_currentuser.middleware import (get_current_authenticated_user)


from eqs.models import DepartmentForEq
from rise_info.baseModels import BaseManager
from rise_info.choices import InfoTypeChoices
# Create your models here.


class RoleInLocal(models.Model):
    name = models.CharField(
        verbose_name='現地担当名', null=False, max_length=16,
        blank=False, help_text='例:信頼性担当者, APPS担当者'
    )
    helpTXT = models.TextField(
        verbose_name='現地担当補足説明', null=True, blank=False, max_length=128,
        help_text='例：信頼性担当者は本信頼性ホームページの配信先管理をお願いします。'
    )

    def __str__(self):
        return self.name


class InfoTypeRelationRole(models.Model):
    info_type = models.CharField(
        verbose_name='情報種別', max_length=16, choices=InfoTypeChoices.choices,
        default=InfoTypeChoices.TECHINICAL, null=False, blank=False
    )
    role = models.ForeignKey(
        RoleInLocal,
        verbose_name='現地担当名', related_name='info_type_relations', on_delete=models.CASCADE)


class Addresses(models.Model):
    object = BaseManager()
    name = models.CharField(verbose_name='氏名', null=False,
                            blank=False, max_length=16)
    position = models.CharField(
        verbose_name='役職', null=False, blank=False, max_length=16)
    mail = models.EmailField(verbose_name='メールアドレス', null=False, blank=False)
    is_HTML_mail = models.BooleanField(
        verbose_name='HTML形式による送信可否', default=False,
        help_text='テキスト形式が望ましい場合はチェックを外してください'
    )
    role = models.ManyToManyField(
        RoleInLocal, verbose_name='現地担当名', null=True, blank=True,
        related_name='addresses')
    groups = models.ManyToManyField(
        Group,
        verbose_name='障害通報書配信元官署グループ', related_name='addresses', blank=True,
        help_text='受け取りたい障害通報書の発行官署の選択'
    )
    department = models.ManyToManyField(
        DepartmentForEq,
        verbose_name='担当装置分類', related_name='addresses', blank=True,
        help_text='受け取りたい障害通報書の担当装置分類の選択'
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
