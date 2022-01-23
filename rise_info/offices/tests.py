from django import shortcuts
from django.test import TestCase, tag
from django.contrib.auth.models import User

from datetime import datetime as dt
import pytz
import shutil
import os

from accounts.tests import login
from .models import Office, offices_csv_import
from histories.models import getLastUpdateAt
from histories.models import getLastUpdateAt

mock_update_at = dt(2019,7,15,15,22,48,0, pytz.timezone('Asia/Tokyo'))
mock_update_at2 = dt(2001,1,1,0,0,0,0, pytz.timezone('Asia/Tokyo'))

class NoLoginOfficeListTest(TestCase):
    def test_no_login_office_list_return_402_and_expected_title(self) -> None:
        response = self.client.get("/offices/")
        self.assertEqual(response.status_code, 302)

class OfficeListTest(TestCase):
    def setUp(self) -> None:
        login(self)

    def test_office_list_return_200_and_expected_title(self) -> None:
        response = self.client.get("/offices/")
        self.assertContains(response,"官署・アカウント一括更新" , status_code=200)    

    def test_office_list_uses_expected_template(self):
        response = self.client.get("/offices/")
        self.assertTemplateUsed(response, "offices/upload.html")

class OfficeDelTest(TestCase):
    def setUp(self) -> None:
        Office.objects.create(id='TEST', name='test000', shortcut_name='tes', update_at=mock_update_at)

    def test_with_login_delete_office(self):
        login(self)
        try:
            office = Office.objects.get(id='TEST')
        except:
            self.fail('あるはずのMockOfficeが取得できない')
        self.client.get('/offices/' + str(office.id) + '/del/')
        office = Office.objects.get_or_none(id='TEST')
        self.assertFalse(office.unyo_sts)

@tag('slowTest')
class OfficeCsvImportTest(TestCase):
    def setUp(self) -> None:
        shutil.copy2('uploads/documents/Offices.csv', 'uploads/documents/Offices_test.csv')
        shutil.copy2('test_data/Offices.csv','uploads/documents/Offices.csv')

    def tearDown(self) -> None:
        shutil.copy2('uploads/documents/Offices_test.csv','uploads/documents/Offices.csv')
        os.remove('uploads/documents/Offices_test.csv')

    def test_csv_import_test(self):
        self.assertEqual(getLastUpdateAt('office'), mock_update_at2)
        self.assertEqual(Office.objects.all().count(), 0)
        self.assertEqual(User.objects.all().count(), 0)
        self.assertEqual(str(getLastUpdateAt('office').tzinfo),'Asia/Tokyo') 

        offices_csv_import()
        self.assertLess(0, Office.objects.all().count())
        self.assertLess(0, User.objects.all().count())
        self.assertEqual(mock_update_at, getLastUpdateAt('office'))  
