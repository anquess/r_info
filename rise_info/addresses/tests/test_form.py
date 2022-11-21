from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from ..forms import AddressesForm
from ..models import Addresses
from accounts.tests.com_setup import login
from offices.tests.test_model import make_mock_office, make_mock_offices_group

import random
import string

test_dir_path = '/home/pi/django/rise_info/test_data/'


def randomname(length, charactors=string.ascii_letters + string.digits):
    randlst = [random.choice(charactors)
               for i in range(length)]
    return ''.join(randlst)


def make_mock_right_param(testCase: TestCase):
    text_len_16 = randomname(16)
    text_mail_addr = "abc@abc.com"
    grp = (make_mock_offices_group(), make_mock_offices_group())
    offices = (make_mock_office(grp), make_mock_office())
    testCase.params = {
        'name': text_len_16,
        'position': text_len_16,
        'mail': text_mail_addr,
        'offices': offices,
        'offices_groups': grp,
        'is_required_when_send_mail': False,
    }


def make_mock_wrong_param(testCase: TestCase):
    text_len_17 = randomname(17)
    wrong_text_mail_addr = 'aaa'
    testCase.wrong_params = {
        'name': text_len_17,
        'position': text_len_17,
        'mail': wrong_text_mail_addr,
    }


class AddressesFormTests(TestCase):
    def setUp(self) -> None:
        make_mock_right_param(self)
        make_mock_wrong_param(self)
        return super().setUp()

    def test_valid_true(self):
        address = Addresses()
        form = AddressesForm(self.params, instance=address)
        self.assertTrue(form.is_valid())

    def test_valid_when_param_in_None(self):
        params = {}
        address = Addresses()
        form = AddressesForm(params, instance=address)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['name'][0], '氏名は必須です')
        self.assertEqual(form.errors['position'][0], '役職は必須です')
        self.assertEqual(form.errors['mail'][0], 'メールアドレスは必須です')

    def test_valid_when_too_long(self):
        address = Addresses()
        form = AddressesForm(self.wrong_params, instance=address)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['name'][0], '氏名は16文字以内です。')
        self.assertEqual(form.errors['position'][0], '役職は16文字以内です。')
        self.assertEqual(form.errors['mail'][0], '有効なメールアドレスを入力してください。')
