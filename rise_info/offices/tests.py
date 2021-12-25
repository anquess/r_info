from django import shortcuts
from django.test import TestCase, tag
from django.contrib.auth.models import User

from datetime import datetime as dt
import pytz

from accounts.tests import login
from .models import Office, offices_csv_import
from histories.models import getLastUpdateAt

mock_update_at = dt(2001,1,1,0,0,0,0)
mock_update_at2 = dt(2001,1,1,0,0,0,0,pytz.timezone('Asia/Tokyo'))

class NoLoginOfficeListTest(TestCase):
    def test_no_login_office_list_return_402_and_expected_title(self) -> None:
        response = self.client.get("/offices/")
        self.assertEqual(response.status_code, 302)

class OfficeListTest(TestCase):
    def setUp(self) -> None:
        login(self)

    def test_office_list_return_200_and_expected_title(self) -> None:
        response = self.client.get("/offices/")
        self.assertContains(response,"ファイルをアップロード" , status_code=200)    

    def test_info_list_uses_expected_template(self):
        response = self.client.get("/offices/")
        self.assertTemplateUsed(response, "offices/upload.html")

class OfficeDelTest(TestCase):
    def setUp(self) -> None:
        Office.objects.create(slug='test', name='test000', shortcut_name='tes', update_at=mock_update_at)

    def test_with_login_delete_office(self):
        login(self)
        try:
            office = Office.objects.get(slug='test')
        except:
            self.fail('あるはずのMockOfficeが取得できない')
        self.client.get('/offices/' + str(office.pk) + '/del/')
        office = Office.objects.get_or_none(slug='test')
        self.assertIsNone(office)

@tag('slowTest')
class OfficeCsvImportTest(TestCase):
    def test_csv_import_test(self):
        self.assertEqual(getLastUpdateAt('office'), mock_update_at)
        self.assertEqual(Office.objects.all().count(), 0)
        self.assertEqual(User.objects.all().count(), 0)
        offices_csv_import()
        self.assertLess(0, Office.objects.all().count())
        self.assertLess(0, User.objects.all().count())
        self.assertLess(mock_update_at2, getLastUpdateAt('office'))        
