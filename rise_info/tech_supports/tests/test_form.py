from django.test import TestCase

from ..forms import TechSupportsForm, TechSupportCommentsForm
from ..models import TechSupports, TechSupportComments
from accounts.tests.com_setup import login
from eqs.tests.test_model import make_mock_eqtypes
from infos.tests.test_form import randomfile

import os
import random
import string


test_dir_path = '/home/pi/django/rise_info/test_data/'


def randomname(length, charactors=string.ascii_letters + string.digits):
    randlst = [random.choice(charactors)
               for i in range(length)]
    return ''.join(randlst)


def make_mock_right_param(testCase: TestCase):
    text_len_128 = randomname(128)
    text_len_4096 = randomname(4096)
    text_len_2048 = randomname(2048)
    eq_types = (make_mock_eqtypes(), make_mock_eqtypes())
    testCase.params = {
        'title': text_len_128,
        'content': text_len_4096,
        'is_rich_text': True,
        'inquiry': text_len_2048,
        'eqtypes': eq_types,
        'select_register': 'not_registered',
        'info_type': 'support',
    }


def make_mock_wrong_param(testCase: TestCase):
    text_len_129 = randomname(129)
    text_len_4097 = randomname(4097)
    text_len_2049 = randomname(2049)
    testCase.wrong_params = {
        'title': text_len_129,
        'content': text_len_4097,
        'is_rich_text': True,
        'inquiry': text_len_2049,
        'select_register': 'register',
        'info_type': 'support',
    }


def mock_tech_support(testCase):
    return TechSupports.objects.create(
        title=testCase.params['title'],
        content=testCase.params['content'],
        is_rich_text=testCase.params['is_rich_text'],
        inquiry=testCase.params['inquiry'],
        select_register=testCase.params['select_register'],
    )


class EqtypesFormTests(TestCase):
    def setUp(self) -> None:
        make_mock_right_param(self)
        make_mock_wrong_param(self)
        return super().setUp()

    def test_valid_true(self):
        techSupports = TechSupports()
        form = TechSupportsForm(self.params, instance=techSupports)
        self.assertTrue(form.is_valid())

    def test_valid_when_param_in_None(self):
        params = {}
        techSupports = TechSupports()
        form = TechSupportsForm(params, instance=techSupports)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['title'][0], 'タイトルは必須です')
        self.assertEqual(form.errors['select_register'][0], 'この項目は必須です。')
        self.assertEqual(form.errors['eqtypes'][0], '装置型式は必須です')
        self.assertEqual(len(form.errors), 4)

    def test_valid_when_too_long(self):
        techSupports = TechSupports()
        form = TechSupportsForm(self.wrong_params, instance=techSupports)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['title'][0], 'タイトルは128文字以内です')
        self.assertEqual(form.errors['content'][0], '内容は4096文字以内です')
        self.assertEqual(form.errors['inquiry'][0], '概要は2048文字以内です')
        self.assertEqual(form.errors['eqtypes'][0], '装置型式は必須です')
        self.assertEqual(len(form.errors), 4)


class TechSupportCommentsFormTests(TestCase):
    def setUp(self) -> None:
        login(self)
        make_mock_right_param(self)
        self.info = mock_tech_support(self)
        self.max_file = randomfile(9, "mb")
        self.over_file = randomfile(10, "mb")
        return super().setUp()

    def tearDown(self) -> None:
        os.remove(test_dir_path + str(self.max_file.name))
        os.remove(test_dir_path + str(self.over_file.name))

    def test_valid_true(self):
        text_len_512 = randomname(512)
        params = {
            'comment_txt': text_len_512,
            'info': self.info,
        }
        data = {'file': self.max_file}
        comment = TechSupportComments()
        form = TechSupportCommentsForm(params, data, instance=comment)
        result = form.is_valid()
        self.assertTrue(result)

    def test_valid_when_param_is_none(self):
        params = {}
        comment = TechSupportComments()
        form = TechSupportCommentsForm(params, instance=comment)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['info'][0], 'infoは必須です')
        self.assertEqual(form.errors['comment_txt'][0], 'コメントは必須です')

    def test_valid_when_too_long(self):
        text_len_513 = randomname(513)
        params = {
            'comment_txt': text_len_513,
            'info': self.info,
        }
        data = {'file': self.over_file}
        comment = TechSupportComments()
        form = TechSupportCommentsForm(params, data, instance=comment)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['comment_txt'][0], 'コメントは512文字以内です')
        self.assertEqual(form.errors['file'][0], 'アップロードファイルは10MB未満にしてください')
