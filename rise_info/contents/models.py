from django.db import models

# Create your models here.


class Menu(models.Model):
    menu_title = models.CharField('タイトル', max_length=24)
    sort_num = models.IntegerField('並び順', unique=True)
