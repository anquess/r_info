from django.test import TestCase

from datetime import datetime as dt
import pytz

from accounts.tests.com_setup import login
from ..models import Office

mock_update_at = dt(2019,7,15,15,22,48,0, pytz.timezone('Asia/Tokyo'))

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
