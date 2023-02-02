from django.db import models


class ConfirmationTypeChoices(models.TextChoices):
    UNNECESSASY = 'unnecessary', '確認不要'
    CONFIRMED = 'confirmed', '確認済'
    CHECKING_NOW = 'checking_now', '確認中'


class InfoTypeChoices(models.TextChoices):
    TECHINICAL = 'technical', '技術情報'
    FAILURE_CASE = 'failure_case', '障害情報'
    SAFETY = 'safety', '安全情報事例'
    EVENT = 'event', 'イベント情報'
    MANUAL = 'manual', '完成図書差替'
    APPS = 'apps', 'APPS'
    FOLLOW = 'follow', '整備フォロー体制'


class InfoTypeChoicesSupo(models.TextChoices):
    SUPPORT = 'support', '技術支援'
    IMPROVEMENT_PLAN = 'improvement', '技術改善提案'
    PUBLIC_RELATION = 'pr', '情報発信'
    ETC = 'etc', 'その他'


class IsConfirmChoices(models.TextChoices):
    NONE = 'none', '無'
    YES = 'yes', '有'
    CHECKING_NOW = 'checking_now', '確認中'


class RegisterStatusChoices(models.TextChoices):
    NOT_REGISTERED = 'not_registered', '未登録'
    UNDER_RENEWAL = 'under_renewal', '更新中'
    REGISTER = 'register', '登録済'
    TEMP = 'temp', '仮登録'


class RegisterStatusChoicesFailuer(models.TextChoices):
    TEMP = 'temporaty', '一時保存'
    SENDED = 'sended', '送信済み'
    DONE = 'done', '解決済'


class RegisterStatusChoicesSupo(models.TextChoices):
    NOT_REGISTERED = 'not_registered', '未登録'
    REGISTER = 'register', '登録依頼中'
    TEMP = 'temporaty', '一時保存'
    DOING = 'doing', '登録受付完了 対応中'
    DONE = 'done', '解決済'
