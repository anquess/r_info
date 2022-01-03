from django.test import TestCase
from django.urls import resolve, reverse
from django.core.files.base import File

from .models import FailuerReport, AttachmentFile
from .views import failuer_report_edit
from accounts.tests import loginTestAccount

import shutil
import os

def addMockFailuereReports(testCase) -> None:
    data = {'title': 'タイトル', 'sammary': '概要'}
    testCase.response = testCase.client.post("/failuer_reports/new/", data)

def detail_and_edit_common_setUp(testCase, isEdit:bool):
    loginTestAccount(testCase)
    addMockFailuereReports(testCase)
    info = FailuerReport.objects.get_or_none(title="タイトル")
    if info:
        if isEdit:
            testCase.response = testCase.client.get("/failuer_reports/%s/edit/" % info.id)        
        else:
            testCase.response = testCase.client.get("/failuer_reports/%s/" % info.id)
    else:
        testCase.fail('あるはずのMockInfoが見つからない')


class FaluerReportsListTest(TestCase):
    def setUp(self) -> None:
        loginTestAccount(self)
    
    def test_failuer_report_list_return_200_and_expected_title(self) -> None:
        response = self.client.get("/failuer_reports/")
        self.assertContains(response, "障害通報一覧" , status_code=200)
        
    def test_failuer_report_list_uses_expected_template(self) ->None:
        response = self.client.get("/failuer_reports/")
        self.assertTemplateUsed(response, "failuer_reports/list.html")

class CreateFailureReportTest(TestCase):
    def setUp(self) -> None:
        loginTestAccount(self)

    def test_render_creation_form(self):
        response = self.client.get("/failuer_reports/new/")
        self.assertContains(response, "障害通報の登録", status_code=200)

    def test_create_failuer_report(self):
        addMockFailuereReports(self)
        info = FailuerReport.objects.get(title='タイトル')
        self.assertEqual('概要', info.sammary)

class FailuerReportsDetailTest(TestCase):
    def setUp(self) -> None:
        detail_and_edit_common_setUp(self, False)

    def test_should_use_expected_template(self):
        self.assertTemplateUsed(self.response, "failuer_reports/detail.html")
    def test_detail_page_returns_200_and_expected_heading(self):
        self.assertContains(self.response, "タイトル", status_code=200)

class EditFailuerReportsTest(TestCase):
    def setUp(self) -> None:
        detail_and_edit_common_setUp(self, True)

    def test_should_use_expected_template(self):
        self.assertTemplateUsed(self.response, "failuer_reports/edit.html")

class DetailFailuerReportsTest(TestCase):
    def test_should_resolve_info_edit(self):
        found = resolve("/failuer_reports/1/edit/")
        self.assertEqual(failuer_report_edit, found.func)

class InfoModelTest(TestCase):
    def test_is_empty(self) -> None:
        infos = FailuerReport.objects.all()
        self.assertEqual(infos.count(), 0)

class InfoDelTest(TestCase):
    def setUp(self) -> None:
        loginTestAccount(self)
        addMockFailuereReports(self)

    def test_info_del_count(self):
        try:
            info = FailuerReport.objects.get(title='タイトル')
        except:
            self.fail('あるはずのmockInfoが見つからない')
        response = self.client.get("/failuer_reports/" + str(info.pk) + "/del/")
        self.assertRedirects(response, reverse('failuer_report_list') , status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

        try:
            info = FailuerReport.objects.get(title='タイトル')
        except:
            return None
        self.fail('ないはずのmockInfoが見つかった')

class AddReportAttachmentFileTest(TestCase):
    def setUp(self) -> None:
        loginTestAccount(self)
        addMockFailuereReports(self)
        shutil.copy('uploads/sorry.jpg','abc.jpg')
        shutil.copy('uploads/user.png','abc.png')
        try:
            self.info = FailuerReport.objects.get(title='タイトル')
        except:
            self.fail('あるはずのmockReportsが見つからない')
        if not os.path.isfile("abc.jpg"):
            self.fail('mockReportAttachmentFilesファイル(abc.jpg)が見つからない')
        self.info_attach = AttachmentFile.objects.create(info=self.info, file=File(open('abc.jpg','rb')))
    def tearDown(self) -> None:
        os.remove('abc.jpg')
        os.remove('abc.png')
        return super().tearDown()
    def test_create_report_attachment(self):
        self.assertTrue(os.path.isfile(f"uploads/fail_rep/{str(self.info.pk)}/{str(self.info_attach.pk)}/abc.jpg"))
        self.info_attach.file = File(open('abc.png','rb'))
        self.info_attach.save()
        self.assertFalse(os.path.isfile(f"uploads/fail_rep/{str(self.info.pk)}/{str(self.info_attach.pk)}/abc.jpg"))
        os.remove(f"uploads/fail_rep/{str(self.info.pk)}/{str(self.info_attach.pk)}/abc.png")
