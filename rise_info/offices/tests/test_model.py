from django.test import TestCase, tag
from django.contrib.auth.models import User

from datetime import datetime as dt
import pytz
import shutil
import os
import random
import string

from ..models import Office, OfficesGroup, offices_csv_import
from histories.models import getLastUpdateAt

mock_update_at = dt(2019, 7, 15, 15, 22, 48, 0, pytz.timezone('Asia/Tokyo'))
mock_update_at2 = dt(2001, 1, 1, 0, 0, 0, 0, pytz.timezone('Asia/Tokyo'))


def randomname(length, charactors=string.ascii_letters + string.digits):
    randlst = [random.choice(charactors) for i in range(length)]
    return ''.join(randlst)


def make_mock_offices_group():
    grp = OfficesGroup.objects.create(
        group_name=randomname(32),
    )
    grp.save()
    return grp


def make_mock_office(grp=None):

    office = Office.objects.create(
        id=randomname(1, string.ascii_uppercase) +
        randomname(3, string.digits),
        name=randomname(32),
        shortcut_name=randomname(8),
        update_at=mock_update_at
    )
    office.save()
    if grp:
        office.offices_group.set(grp)
        office.save()
    return office


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
