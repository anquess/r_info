from django.test import TestCase
from django.urls import resolve
from django.core.files.base import File

import os
import shutil

from infos.views import info_edit
from infos.models import Info, InfoAttachmentFile
from accounts.tests import login

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
        self.assertTemplateUsed(response, "infos/list.html")

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

def detail_and_edit_common_setUp(testCase, isEdit:bool):
    login(testCase)
    addMockInfo(testCase)
    info = Info.objects.get_or_none(title="タイトル")
    if info:
        if isEdit:
            testCase.response = testCase.client.get("/infos/%s/edit/" % info.id)        
        else:
            testCase.response = testCase.client.get("/infos/%s/" % info.id)
    else:
        testCase.fail('あるはずのMockInfoが見つからない')


class InfoDetailTest(TestCase):
    def setUp(self) -> None:
        detail_and_edit_common_setUp(self, False)

    def test_should_use_expected_template(self):
        self.assertTemplateUsed(self.response, "infos/detail.html")
    def test_detail_page_returns_200_and_expected_heading(self):
        self.assertContains(self.response, "タイトル", status_code=200)

class EditInfoTest(TestCase):
    def setUp(self) -> None:
        detail_and_edit_common_setUp(self, True)

    def test_should_use_expected_template(self):
        self.assertTemplateUsed(self.response, "infos/edit.html")

class DetailInfoTest(TestCase):
    def test_should_resolve_info_edit(self):
        found = resolve("/infos/1/edit/")
        self.assertEqual(info_edit, found.func)

class InfoModelTest(TestCase):
    def test_is_empty(self) -> None:
        infos = Info.objects.all()
        self.assertEqual(infos.count(), 0)

class InfoDelTest(TestCase):
    def setUp(self) -> None:
        login(self)
        addMockInfo(self)

    def test_info_del_count(self):
        try:
            info = Info.objects.get(title='タイトル')
        except:
            self.fail('あるはずのmockInfoが見つからない')
        self.client.get("/infos/" + str(info.pk) + "/del/")
        try:
            info = Info.objects.get(title='タイトル')
        except:
            return None
        self.fail('ないはずのmockInfoが見つかった')

class AddInfoAttachmentTest(TestCase):
    def setUp(self) -> None:
        login(self)
        addMockInfo(self)
        shutil.copy('uploads/sorry.jpg','abc.jpg')
        shutil.copy('uploads/user.png','abc.png')
    def tearDown(self) -> None:
        os.remove('abc.jpg')
        os.remove('abc.png')
        return super().tearDown()
    def test_create_info_attachment(self):
        try:
            info = Info.objects.get(title='タイトル')
        except:
            self.fail('あるはずのmockInfoが見つからない')
        if not os.path.isfile("abc.jpg"):
            self.fail('mockInfoAttachmentsファイル(abc.jpg)が見つからない')
        self.info_attach = InfoAttachmentFile.objects.create(info=info, attachment=File(open('abc.jpg','rb')))
        self.assertTrue(os.path.isfile(f"uploads/info/{str(info.pk)}/{str(self.info_attach.pk)}/abc.jpg"))
        self.info_attach.attachment = File(open('abc.png','rb'))
        self.info_attach.save()
        self.assertFalse(os.path.isfile(f"uploads/info/{str(info.pk)}/{str(self.info_attach.pk)}/abc.jpg"))
        os.remove(f"uploads/info/{str(info.pk)}/{str(self.info_attach.pk)}/abc.png")
