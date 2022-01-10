from django import shortcuts
from django.test import TestCase, tag
from django.contrib.auth.models import User

from datetime import datetime as dt
import pytz
import shutil
import os

from accounts.tests import login
from .models import Eqtype, eqtypes_csv_import
from histories.models import getLastUpdateAt

mock_update_at = dt(2001,1,1,0,0,0,0)
mock_update_at2 = dt(2001,1,1,0,0,0,0,pytz.timezone('Asia/Tokyo'))

class NoLoginEqtypeListTest(TestCase):
    def test_no_login_eqtypes_list_return_402_and_expected_title(self) -> None:
        response = self.client.get("/eqs/eqtypes/")
        self.assertEqual(response.status_code, 302)

class EqtypeListTest(TestCase):
    def setUp(self) -> None:
        login(self)

    def test_eqtype_list_return_200_and_expected_title(self) -> None:
        response = self.client.get("/eqs/eqtypes/")
        self.assertContains(response,"装置型式一括更新" , status_code=200)    

    def test_eqtype_list_uses_expected_template(self):
        response = self.client.get("/eqs/eqtypes/")
        self.assertTemplateUsed(response, "eqs/eqtypes/upload.html")

class EqtypeDelTest(TestCase):
    def setUp(self) -> None:
        Eqtype.objects.create(id='TEST', slug="abc", create_at=mock_update_at)

    def test_with_login_delete_office(self):
        login(self)
        try:
            eqtype = Eqtype.objects.get(id='TEST')
        except:
            self.fail('あるはずのMockOfficeが取得できない')
        response = self.client.get('/eqs/eqtypes/' + str(eqtype.slug) + '/del/')
        self.assertEqual(response.status_code, 302)
        eqtype2 = Eqtype.objects.get_or_none(id='TEST')
        self.assertEqual(eqtype2, None)

@tag('slowTest')
class EqtypeCsvImportTest(TestCase):
    def setUp(self) -> None:
        shutil.copy2('uploads/documents/EQTypes.csv', 'uploads/documents/EQTypes_test.csv')
        shutil.copy2('test_data/EQTypes.csv','uploads/documents/EQTypes.csv')

    def tearDown(self) -> None:
        shutil.copy2('uploads/documents/EQTypes_test.csv','uploads/documents/EQTypes.csv')
        os.remove('uploads/documents/EQTypes_test.csv')

    def test_csv_import_test(self):
        self.assertEqual(getLastUpdateAt('eqtype'), mock_update_at)
        self.assertEqual(Eqtype.objects.all().count(), 0)
        eqtypes_csv_import()
        self.assertLess(0, Eqtype.objects.all().count())
        self.assertLess(mock_update_at2, getLastUpdateAt('eqtype'))        
