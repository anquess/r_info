from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve

from infos.views import info_edit
from infos.models import Info
from accounts.tests import login

UserModel = get_user_model()

def addMockInfo(testCase) -> None:
    testCase.client.force_login(testCase.user)
    data = {'title': 'タイトル', 'sammary': '概要'}
    testCase.response = testCase.client.post("/infos/new/", data)
    

class InfoListTest(TestCase):
    def setUp(self) -> None:
        login(self)
    
    def test_info_list_return_200_and_expected_title(self) -> None:
        response = self.client.get("/infos/")
        self.assertContains(response, "信頼性情報一覧" , status_code=200)
        
    def test_info_list_uses_expected_template(self) ->None:
        response = self.client.get("/infos/")
        self.assertTemplateUsed(response, "infos/info_list.html")

class CreateInfoTest(TestCase):
    def setUp(self) -> None:
        login(self)

    def test_render_creation_form(self):
        response = self.client.get("/infos/new/")
        self.assertContains(response, "信頼性情報の登録", status_code=200)

    def test_create_info(self):
        addMockInfo(self)
        info = Info.objects.get(title='タイトル')
        self.assertEqual('概要', info.sammary)

class InfoDetailTest(TestCase):
    def setUp(self) -> None:
        login(self)
        addMockInfo(self)

    def test_should_use_expected_template(self):
        response = self.client.get(self.response.url)
        self.assertTemplateUsed(response, "infos/info_detail.html")

    def test_detail_page_returns_200_and_expected_heading(self):
        response = self.client.get(self.response.url)
        self.assertContains(response, "タイトル", status_code=200)

class EditInfoTest(TestCase):
    def setUp(self) -> None:
        login(self)
        addMockInfo(self)

    def test_should_use_expected_template(self):
        response = self.client.get(self.response.url + 'edit/')
        self.assertTemplateUsed(response, "infos/info_edit.html")

class DetailInfoTest(TestCase):
    def test_should_resolve_info_edit(self):
        found = resolve("/infos/1/edit/")
        self.assertEqual(info_edit, found.func)

class InfoModelTest(TestCase):
    def test_is_empty(self) -> None:
        infos = Info.objects.all()
        self.assertEqual(infos.count(), 0)