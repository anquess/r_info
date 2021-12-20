from datetime import datetime
from unittest import mock
from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.urls import resolve

from infos.views import info_list, info_edit
from infos.models import Info
from accounts.tests import testAcountCreate, login

UserModel = get_user_model()
mock_date = datetime(2021, 3, 4, 14, 57, 11, 703055)

#def addMockOffice(testCase) -> None:
#    if not hasattr(testCase, 'user'):
#        testAcountCreate(testCase)
#    import warnings
#    warnings.simplefilter('ignore')
#    with mock.patch('django.utils.timezone.now') as mock_now:
#        mock_now.return_value = mock_date
#        testCase.info = Info.objects.create(
#            title="title1",
#            sammary="print('hello')",
#        )

#class OfficeListTest(TestCase):
#    def test_office_list_return_200_and_expected_title(self) -> None:
#        response = self.client.get("/offices/")
#        self.assertContains(response,"官署一覧" , status_code=200)    
#
#    def test_info_list_uses_expected_template(self):
#        response = self.client.get("/offices/")
#        self.assertTemplateUsed(response, "offices/office_list.html")

#class OfficeListRenderInfosTest(TestCase):
#    def setUp(self) -> None:
#        addMockOffice(self)
#
#    def test_should_return_info_title(self) -> None:
#        request = RequestFactory().get("/infos/")
#        response = info_list(request)
#        self.assertContains(response, 'title', status_code=200)
#
#class CreateInfoTest(TestCase):
#    def setUp(self) -> None:
#        login(self)
#
#    def test_render_creation_form(self):
#        response = self.client.get("/infos/new/")
#        self.assertContains(response, "信頼性情報の登録", status_code=200)
#
#    def test_create_info(self):
#        self.client.force_login(self.user)
#        data = {'title': 'タイトル', 'sammary': '概要'}
#        self.client.post("/infos/new/", data)
#        info = Info.objects.get(title='タイトル')
#        self.assertEqual('概要', info.sammary)
#
#class InfoDetailTest(TestCase):
#    def setUp(self) -> None:
#        addMockInfo(self)
#        login(self)
#
#    def test_should_use_expected_template(self):
#        response = self.client.get("/infos/%s/" % self.info.id)
#        self.assertTemplateUsed(response, "infos/info_detail.html")
#    def test_detail_page_returns_200_and_expected_heading(self):
#        response = self.client.get("/infos/%s/" % self.info.id)
#        self.assertContains(response, "title1", status_code=200)
#
#class EditInfoTest(TestCase):
#    def setUp(self) -> None:
#        addMockInfo(self)
#        login(self)
#
#    def test_should_use_expected_template(self):
#        response = self.client.get("/infos/%s/edit/" % self.info.id)
#        self.assertTemplateUsed(response, "infos/info_edit.html")
#
#class DetailInfoTest(TestCase):
#    def test_should_resolve_info_edit(self):
#        found = resolve("/infos/1/edit/")
#        self.assertEqual(info_edit, found.func)
#
#class InfoModelTest(TestCase):
#    def test_is_empty(self) -> None:
#        infos = Info.objects.all()
#        self.assertEqual(infos.count(), 0)
#    
#    def test_create_at_now(self) -> None:
#        addMockInfo(self)
#        self.assertEqual(self.info.created_at, mock_date)
#        self.assertEqual(self.info.updated_at, mock_date)
#