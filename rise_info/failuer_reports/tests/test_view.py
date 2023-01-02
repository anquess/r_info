from django.test import TestCase
from django.urls import resolve, reverse
from django.core.files.base import File

from ..models import FailuerReport, AttachmentFile, FailuerReportRelation
from ..views import failuer_report_edit
from .test_form import getCollectParams
from accounts.tests.com_setup import loginTestAccount
from eqs.models import DepartmentForEq

import shutil
import os
from datetime import datetime


def addMockFailuereReports(testCase) -> None:
    testCase.params = getCollectParams()
    testCase.params['attachmentfile_set-TOTAL_FORMS'] = 0
    testCase.params['attachmentfile_set-INITIAL_FORMS'] = 0
    testCase.params['circumstances_set-TOTAL_FORMS'] = 0
    testCase.params['circumstances_set-INITIAL_FORMS'] = 0
    testCase.response = testCase.client.post(
        "/failuer_reports/new/", testCase.params)


def detail_and_edit_common_setUp(testCase, isEdit: bool):
    loginTestAccount(testCase)
    addMockFailuereReports(testCase)
    testCase.assertRedirects(
        testCase.response, reverse('failuer_report_list'), status_code=302,
        target_status_code=200, msg_prefix='', fetch_redirect_response=True)
    info = FailuerReportRelation.objects.get_or_none(
        title=testCase.params['title'])
    if info:
        if isEdit:
            testCase.response = testCase.client.get(
                "/failuer_reports/%s/edit/" % info.id)
        else:
            testCase.response = testCase.client.get(
                "/failuer_reports/%s/" % info.id)
    else:
        testCase.fail('あるはずのMockInfoが見つからない')


class FaluerReportsListTest(TestCase):
    def setUp(self) -> None:
        loginTestAccount(self)

    def test_failuer_report_list_return_200_and_expected_title(self) -> None:
        response = self.client.get("/failuer_reports/")
        self.assertContains(response, "障害通報一覧", status_code=200)

    def test_failuer_report_list_uses_expected_template(self) -> None:
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
        info = FailuerReportRelation.objects.get_or_none(
            title=self.params['title'])
        if info:
            self.assertEqual(self.params['sammary'],
                             info.failuerreport_ptr.sammary)
        else:
            self.fail('障害通報が登録されていない')


class FailuerReportsDetailTest(TestCase):
    def setUp(self) -> None:
        detail_and_edit_common_setUp(self, False)

    def test_should_use_expected_template(self):
        self.assertTemplateUsed(self.response, "failuer_reports/detail.html")

    def test_detail_page_returns_200_and_expected_heading(self):
        self.assertContains(
            self.response, self.params['title'], status_code=200)


class EditFailuerReportsTest(TestCase):
    def setUp(self) -> None:
        detail_and_edit_common_setUp(self, True)

    def test_should_use_expected_template(self):
        self.assertTemplateUsed(self.response, "failuer_reports/edit.html")


class DetailFailuerReportsTest(TestCase):
    def test_should_resolve_info_edit(self):
        found = resolve("/failuer_reports/1/edit/")
        self.assertEqual(failuer_report_edit, found.func)


class InfoDelTest(TestCase):
    def setUp(self) -> None:
        loginTestAccount(self)
        addMockFailuereReports(self)

    def test_info_del_count(self):
        info = FailuerReportRelation.objects.get_or_none(
            title=self.params['title'])
        if info:
            response = self.client.get(
                "/failuer_reports/" + str(info.pk) + "/del/")
            self.assertRedirects(response, reverse('failuer_report_list'), status_code=302,
                                 target_status_code=200, msg_prefix='', fetch_redirect_response=True)
        else:
            self.fail('あるはずのmockInfoが見つからない')

        try:
            info = FailuerReport.objects.get_or_none(
                title=self.params['title'])
        except:
            return None
        if info:
            self.fail('ないはずのmockInfoが見つかった')


class AddReportAttachmentFileTest(TestCase):
    def setUp(self) -> None:
        loginTestAccount(self)
        addMockFailuereReports(self)
        shutil.copy('uploads/sorry.jpg', 'abc.jpg')
        shutil.copy('uploads/user.png', 'abc.png')
        self.info = FailuerReport.objects.get_or_none(
            title=self.params['title'])
        if not self.info:
            self.fail('あるはずのmockReportsが見つからない')
        if not os.path.isfile("abc.jpg"):
            self.fail('mockReportAttachmentFilesファイル(abc.jpg)が見つからない')
        self.info_attach = AttachmentFile.objects.create(
            info=self.info, file=File(open('abc.jpg', 'rb')))

    def tearDown(self) -> None:
        os.remove('abc.jpg')
        os.remove('abc.png')
        return super().tearDown()

    def test_create_report_attachment(self):
        self.assertTrue(os.path.isfile(
            f"uploads/fail_rep/{str(self.info.pk)}/{str(self.info_attach.pk)}/abc.jpg"))
        self.info_attach.file = File(open('abc.png', 'rb'))
        self.info_attach.save()
        self.assertFalse(os.path.isfile(
            f"uploads/fail_rep/{str(self.info.pk)}/{str(self.info_attach.pk)}/abc.jpg"))
        os.remove(
            f"uploads/fail_rep/{str(self.info.pk)}/{str(self.info_attach.pk)}/abc.png")
