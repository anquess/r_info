from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from ..forms import ContentsForm  # , ContentCommentsForm,
from ..models import ContentsRelation  # , ContentComments
from .test_model import mock_menu  # , mock_content, ContentsCommentTest,
#from accounts.tests.com_setup import login

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


def get_right_params(testCase):
    text_len_128 = randomname(128)
    text_len_4096 = randomname(4096)
    return {
        'title': text_len_128,
        'content': text_len_4096,
        'menu': testCase.menu_1,
        'select_register': 'register',
    }


class ContentFormTests(TestCase):
    def setUp(self) -> None:
        mock_menu(self)

    def test_valid_true(self):
        params = get_right_params(self)
        content = ContentsRelation()
        form = ContentsForm(params, instance=content)
        self.assertTrue(form.is_valid())

    def test_valid_when_param_in_None(self):
        params = {}
        info = ContentsRelation()
        form = ContentsForm(params, instance=info)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['title'][0], 'タイトルは必須です')
        self.assertEqual(form.errors['menu'][0], 'メニューは必須です')

    def test_valid_when_too_long(self):
        text_len_129 = randomname(129)
        text_len_4097 = randomname(4097)
        params = {
            'title': text_len_129,
            'content': text_len_4097,
            'menu': self.menu_1,
        }
        content = ContentsRelation()
        form = ContentsForm(params, instance=content)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['title'][0], 'タイトルは128文字以内です')
        self.assertEqual(form.errors['content'][0], '内容は4096文字以内です')


# class ContentCommentsFormTests(TestCase):
#    max_file = None
#    over_file = None
#
#    def setUp(self) -> None:
#        login(self)
#        mock_content(self)
#        self.max_file = randomfile(9, "mb")
#        self.over_file = randomfile(10, "mb")
#
#    def tearDown(self) -> None:
#        os.remove(test_dir_path + str(self.max_file.name))
#        os.remove(test_dir_path + str(self.over_file.name))
#
#    def test_valid_true(self):
#        text_len_512 = randomname(512)
#        params = {
#            'comment_txt': text_len_512,
#            'content': self.content_1_1,
#        }
#        data = {'file': self.max_file}
#        comment = ContentComments()
#        form = ContentCommentsForm(params, data, instance=comment)
#        self.assertTrue(form.is_valid())
#
#    def test_valid_when_param_is_none(self):
#        params = {}
#        comment = ContentComments()
#        form = ContentCommentsForm(params, instance=comment)
#        self.assertFalse(form.is_valid())
#        self.assertEqual(form.errors['content'][0], 'contentは必須です')
#        self.assertEqual(form.errors['comment_txt'][0], 'コメントは必須です')
#
#    def test_valid_when_too_long(self):
#        text_len_513 = randomname(513)
#        params = {
#            'comment_txt': text_len_513,
#            'content': self.content_1_1,
#        }
#        data = {'file': self.over_file}
#        comment = ContentComments()
#        form = ContentCommentsForm(params, data, instance=comment)
#        self.assertFalse(form.is_valid())
#        self.assertEqual(form.errors['comment_txt'][0], 'コメントは512文字以内です')
#        self.assertEqual(form.errors['file'][0], 'アップロードファイルは10MB未満にしてください')
#
