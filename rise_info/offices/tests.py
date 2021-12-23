from django.test import TestCase
from django.contrib.auth.models import User

from accounts.tests import login
from .models import Office, offices_csv_import

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

class OfficeCsvImportTest(TestCase):
    def test_csv_import_test(self):
        self.assertEqual(Office.objects.all().count(), 0)
        self.assertEqual(User.objects.all().count(), 0)
        offices_csv_import()
        self.assertLess(0, Office.objects.all().count())
        self.assertLess(0, User.objects.all().count())
