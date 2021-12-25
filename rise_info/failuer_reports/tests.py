from django.test import TestCase

from accounts.tests import loginTestAccount

class FaluerReportsListTest(TestCase):
    def setUp(self) -> None:
        loginTestAccount(self)
    
    def test_failuer_report_list_return_200_and_expected_title(self) -> None:
        response = self.client.get("/failuer_reports/")
        self.assertContains(response, "障害通報一覧" , status_code=200)
        
    def test_failuer_report_list_uses_expected_template(self) ->None:
        response = self.client.get("/failuer_reports/")
        self.assertTemplateUsed(response, "failuer_reports/list.html")

