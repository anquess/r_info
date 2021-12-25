from django.test import TestCase

from .models import FailuerReport
from accounts.tests import loginTestAccount

def addMockFailuereReports(testCase) -> None:
    data = {'title': 'タイトル', 'sammary': '概要'}
    testCase.response = testCase.client.post("/failuer_reports/new/", data)

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
