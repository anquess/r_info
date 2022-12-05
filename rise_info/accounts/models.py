from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db import models

from rise_info.baseModels import BaseManager


def createUser(offices):
    user_create_object = []
    user_update_object = []
    for office in offices:
        if User.objects.filter(username=office['username']).exists():
            user = User.objects.get(username=office['username'])
            user.first_name = office['first_name']
            user.last_name = office['last_name']
            user.is_active = office['is_active']
            user_update_object.append(user)
        else:
            user_create_object.append(User(
                username=office['username'],
                first_name=office['first_name'],
                last_name=office['last_name'],
                is_active=office['is_active'],
                password=make_password(office['username'])
            ))
    User.objects.bulk_create(user_create_object)
    User.objects.bulk_update(user_update_object, fields=[
                             'first_name', 'last_name'])


class User_mail_config(models.Model):
    objects = BaseManager()
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_mail_config")
    email_address = models.EmailField(
        verbose_name='送信元アドレス', null=False, blank=False,
        help_text="xxx@mlit.go.jp または、xxx@nyb.mlit.go.jp")
    default_email_header = models.TextField(
        verbose_name='デフォルト送信時メールヘッダー',
        null=True, blank=True, max_length=512,
        help_text="メール本文前段に挿入されます。送信時に変更できます。")
    default_email_footer = models.TextField(
        verbose_name='デフォルト送信時メールフッター',
        null=True, blank=True, max_length=512,
        help_text="メール本文前段に挿入されます。送信時に変更できます。")
