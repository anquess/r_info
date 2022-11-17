from django.db import models
from django_currentuser.db.models import CurrentUserField
from django_currentuser.middleware import (get_current_authenticated_user)


from rise_info.baseModels import BaseManager
from offices.models import Office, OfficesGroup

# Create your models here.


class Addresses(models.Model):
    object = BaseManager()
    name = models.CharField(verbose_name='氏名', null=False,
                            blank=False, max_length=16)
    position = models.CharField(
        verbose_name='役職', null=False, blank=False, max_length=16)
    mail = models.EmailField(verbose_name='メールアドレス', null=False, blank=False)
    is_required_when_send_mail = models.BooleanField(
        verbose_name='送信時必須', default=False)
    offices = models.ManyToManyField(
        Office, verbose_name='配信官署タグ', related_name='addresses', blank=True, help_text='障害通報で登録した官署のタグが1つでもあれば宛先として表示されます')
    offices_groups = models.ManyToManyField(
        OfficesGroup, verbose_name='配信官署タグGRP', related_name='addresses', blank=True)
    created_by = CurrentUserField(verbose_name='登録者', on_update=True,
                                  related_name='%(app_label)s_%(class)s_create', null=False, blank=False)

    def __str__(self):
        return self.position + ' ' + self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_by = get_current_authenticated_user()
        super(Addresses, self).save(*args, **kwargs)

    class Meta:
        db_table = 'addresses'
