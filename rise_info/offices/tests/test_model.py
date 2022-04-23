from django.test import TestCase, tag
from django.contrib.auth.models import User

from datetime import datetime as dt
import pytz
import shutil
import os

from ..models import Office, offices_csv_import
from histories.models import getLastUpdateAt

mock_update_at = dt(2019, 7, 15, 15, 22, 48, 0, pytz.timezone('Asia/Tokyo'))
mock_update_at2 = dt(2001, 1, 1, 0, 0, 0, 0, pytz.timezone('Asia/Tokyo'))


@tag('slowTest')
class OfficeCsvImportTest(TestCase):
    def setUp(self) -> None:
        shutil.copy2('uploads/documents/Offices.csv',
                     'uploads/documents/Offices_test.csv')
        shutil.copy2('test_data/Offices.csv', 'uploads/documents/Offices.csv')

    def tearDown(self) -> None:
        shutil.copy2('uploads/documents/Offices_test.csv',
                     'uploads/documents/Offices.csv')
        os.remove('uploads/documents/Offices_test.csv')

    def test_csv_import_test(self):
        self.assertEqual(getLastUpdateAt('office'), mock_update_at2)
        self.assertEqual(Office.objects.all().count(), 0)
        self.assertEqual(User.objects.all().count(), 0)
        self.assertEqual(str(getLastUpdateAt('office').tzinfo), 'Asia/Tokyo')

        offices_csv_import()
        self.assertLess(0, Office.objects.all().count())
        self.assertLess(0, User.objects.all().count())
        self.assertEqual(mock_update_at, getLastUpdateAt('office'))
