from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from ..forms import InfoForm, InfoCommentsForm
from ..models import Info, InfoComments, InfoTypeChoices
from .test_view import addMockInfo
from accounts.tests.com_setup import login

import datetime
import random
import string
import os

test_dir_path = '/home/pi/django/rise_info/test_data/'


def randomname(length):
    randlst = [random.choice(string.ascii_letters + string.digits)
               for i in range(length)]
    return ''.join(randlst)


def randomfile(val: int, byte_type="mb"):
    assert byte_type in ["b", "kb", "mb", "gb"]
    if byte_type == "b":
        val = val
    elif byte_type == "kb":
        val = 1000 * val
    elif byte_type == "mb":
        val = (1000 ** 2) * val
    elif byte_type == "gb":
        val = (1000 ** 3) * val
    text = ''
    for i in range(val):
        text += '1'
    path = test_dir_path + 'dummy_' + str(val) + str(byte_type) + '.txt'
    if os.path.isfile(path):
        os.remove(path)
    with open(path, 'w') as f:
        print(text, file=f)
    with open(path, 'rb') as f:
        uploadedFile = SimpleUploadedFile(f.name, f.read())
    return uploadedFile


class InfoFormTests(TestCase):
    def test_valid_true(self):
        text_len_128 = randomname(128)
        text_len_32 = randomname(32)
        text_len_4096 = randomname(4096)
        text_len_512 = randomname(512)
        params = {
            'title': text_len_128,
            'info_type': InfoTypeChoices.TECHINICAL,
            'managerID': text_len_32,
            'sammary': text_len_512,
            'content': text_len_4096,
            'select_register': 'register',
            'disclosure_date': datetime.date(2017, 11, 12)
        }
        info = Info()
        form = InfoForm(params, instance=info)
        self.assertTrue(form.is_valid())

    def test_valid_when_param_in_None(self):
        params = {}
        info = Info()
        form = InfoForm(params, instance=info)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['title'][0], 'タイトルは必須です')
        self.assertEqual(form.errors['select_register'][0], 'この項目は必須です。')
        self.assertEqual(form.errors['managerID'][0], '管理番号は必須です')
        self.assertEqual(form.errors['info_type'][0], '情報種別は必須です')
        self.assertEqual(len(form.errors), 4)

    def test_valid_when_too_long(self):
        text_len_33 = randomname(33)
        text_len_129 = randomname(129)
        text_len_513 = randomname(513)
        text_len_4097 = randomname(4097)
        params = {
            'title': text_len_129,
            'info_type': InfoTypeChoices.TECHINICAL,
            'managerID': text_len_33,
            'content': text_len_4097,
            'sammary': text_len_513,
            'select_register': 'register',
            'disclosure_date': datetime.date(2017, 11, 12)
        }
        info = Info()
        form = InfoForm(params, instance=info)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['managerID'][0], '管理番号は32文字以内です')
        self.assertEqual(form.errors['title'][0], 'タイトルは128文字以内です')
        self.assertEqual(form.errors['content'][0], '内容は4096文字以内です')
        self.assertEqual(form.errors['sammary'][0], '概要は512文字以内です')


class InfoCommentsFormTests(TestCase):
    info = None
    max_file = None
    over_file = None

    def setUp(self) -> None:
        login(self)
        addMockInfo(self)
        self.max_file = randomfile(9, "mb")
        self.over_file = randomfile(10, "mb")

        self.info = Info.objects.all()[0]

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
        comment = InfoComments()
        form = InfoCommentsForm(params, data, instance=comment)
        result = form.is_valid()
        print(form.errors)
        self.assertTrue(result)

    def test_valid_when_param_is_none(self):
        params = {}
        comment = InfoComments()
        form = InfoCommentsForm(params, instance=comment)
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
        comment = InfoComments()
        form = InfoCommentsForm(params, data, instance=comment)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['comment_txt'][0], 'コメントは512文字以内です')
        self.assertEqual(form.errors['file'][0], 'アップロードファイルは10MB未満にしてください')
