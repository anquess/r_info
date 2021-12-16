from datetime import datetime
from unittest import mock
from django.test import TestCase
from django.contrib.auth import get_user_model

from infos.models import Info
from accounts.tests import testAcountCreate

UserModel = get_user_model()
mock_date = datetime(2021, 3, 4, 14, 57, 11, 703055)

def addMockInfo(testCase) -> None:
    if not hasattr(testCase, 'user'):
        testAcountCreate(testCase)
    import warnings
    warnings.simplefilter('ignore')
    with mock.patch('django.utils.timezone.now') as mock_now:
        mock_now.return_value = mock_date
        testCase.info = Info.objects.create(
            title="title1",
            sammary="print('hello')",
        )


class InfoModelTest(TestCase):
    def test_is_empty(self) -> None:
        infos = Info.objects.all()
        self.assertEqual(infos.count(), 0)
    
    def test_create_at_now(self) -> None:
        addMockInfo(self)
        self.assertEqual(self.info.created_at, mock_date)
        self.assertEqual(self.info.updated_at, mock_date)
