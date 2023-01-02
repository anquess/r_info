from django.test import TestCase

from ..forms import FailuerReportRelationForm, CircumstancesForm
from ..models import FailuerReportRelation
from eqs.models import DepartmentForEq

import datetime
import random
import string


def randomname(length):
    randlst = [random.choice(string.ascii_letters + string.digits)
               for i in range(length)]
    return ''.join(randlst)


def mockDepartment():
    return DepartmentForEq.objects.create(id="TEST", name='モック')


def getCollectParams():
    text_len_128 = randomname(128)
    text_len_1024 = randomname(1024)
    text_len_4096 = randomname(4096)
    return {
        'title': text_len_128,
        'content': text_len_4096,
        'sammary': text_len_1024,
        'select_register': 'temporaty',
        'failuer_date': datetime.date(2017, 11, 12),
        'failuer_time': datetime.time(12, 10, 10, 10),
        'date_time_confirmation': 'unnecessary',
        'failuer_place': text_len_128,
        'eq': text_len_128,
        'department': [mockDepartment().id],
        'cause': text_len_1024,
        'recovery_propects': text_len_1024,
        'is_flight_impact': 'none',
        'is_press': 'none',
    }


class FailuerReportFormTests(TestCase):
    def test_valid_true(self):
        repo = FailuerReportRelation()
        form = FailuerReportRelationForm(getCollectParams(), instance=repo)
        form.is_valid()
        self.assertEqual(len(form.errors), 0)
        self.assertTrue(form.is_valid())

    def test_valid_when_param_in_None(self):
        params = {}
        repo = FailuerReportRelation()
        form = FailuerReportRelationForm(params, instance=repo)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 11)
        # 1
        self.assertEqual(form.errors['title'][0], 'この項目は必須です。')
        # 2
        self.assertEqual(form.errors['select_register'][0], 'この項目は必須です。')
        # 3
        self.assertEqual(form.errors['failuer_date'][0], '障害発生日は必須です')
        # 4
        self.assertEqual(form.errors['failuer_time'][0], '障害発生時間は必須です')
        # 5
        self.assertEqual(
            form.errors['date_time_confirmation'][0], '発生日時確認状態は必須です')
        # 6
        self.assertEqual(form.errors['failuer_place'][0], '障害発生場所は必須です')
        # 7
        self.assertEqual(form.errors['eq'][0], '障害装置は必須です')
        # 8
        self.assertEqual(form.errors['department']
                         [0], '関係装置分類は配信先の判定に使用するため必須です')
        # 9
        self.assertEqual(form.errors['sammary'][0], '障害概要は必須です')
        # 10
        self.assertEqual(form.errors['is_flight_impact'][0], 'この項目は必須です。')
        # 11
        self.assertEqual(form.errors['is_press'][0], 'この項目は必須です。')

    def test_valid_when_too_long(self):
        text_len_129 = randomname(129)
        text_len_1025 = randomname(1025)
        text_len_4097 = randomname(4097)
        params = {
            'title': text_len_129,
            'content': text_len_4097,
            'sammary': text_len_1025,
            'select_register': 'temporaty',
            'failuer_date': datetime.date(2017, 11, 12),
            'failuer_time': datetime.time(12, 10, 10, 10),
            'date_time_confirmation': 'unnecessary',
            'failuer_place': text_len_129,
            'eq': text_len_129,
            'department': [mockDepartment().id],
            'cause': text_len_1025,
            'recovery_propects': text_len_1025,
            'is_flight_impact': 'none',
            'is_press': 'none',
        }
        repo = FailuerReportRelation()
        form = FailuerReportRelationForm(params, instance=repo)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 7)
        # 1
        self.assertEqual(form.errors['title'][0],
                         'この値は 128 文字以下でなければなりません( 129 文字になっています)。')
        # 2
        self.assertEqual(form.errors['content'][0],
                         '備考は4096文字以内です')
        # 3
        self.assertEqual(form.errors['sammary'][0],
                         '障害概要は1024文字以内です。')
        # 4
        self.assertEqual(form.errors['failuer_place'][0],
                         '障害発生場所は128文字以内です。')
        # 5
        self.assertEqual(form.errors['eq'][0],
                         '障害装置は128文字以内です。')
        # 6
        self.assertEqual(form.errors['cause'][0],
                         '障害原因は1024文字以内です。')
        # 7
        self.assertEqual(form.errors['recovery_propects'][0],
                         '復旧の見通しは1024文字以内です。')
