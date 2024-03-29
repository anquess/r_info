from django.test import TestCase
from django.urls import resolve, reverse


from ..views import support_edit
from ..models import TechSupports
from ..tests.test_form import make_mock_right_param
from accounts.tests.com_setup import login


def addMockTechSupport(testCase) -> None:
    testCase.client.force_login(testCase.user)
    make_mock_right_param(testCase)
    data = {
        'title': testCase.params['title'],
        'content': testCase.params['content'],
        'select_register': testCase.params['select_register'],
        'info_type': testCase.params['info_type'],
        'is_rich_text': testCase.params['is_rich_text'],
        'inquiry': testCase.params['inquiry'],
        'eqtypes': testCase.params['eqtypes'],
        'attachmentfile_set-TOTAL_FORMS': 1,
        'attachmentfile_set-INITIAL_FORMS': 0,
    }
    testCase.response = testCase.client.post(
        "/tech_support/new/", data)


class TechSupportsListTest(TestCase):
    def setUp(self) -> None:
        login(self)

    def test_techSupport_list_return_200_and_expected_title(self) -> None:
        response = self.client.get("/tech_support/")
        self.assertContains(response, "官署発信情報一覧", status_code=200)

    def test_addresse_list_uses_expected_template(self) -> None:
        response = self.client.get("/tech_support/")
        self.assertTemplateUsed(
            response, "tech_supports/tech_support_list.html")


class CreateAddressTest(TestCase):
    def setUp(self) -> None:
        login(self)

    def test_render_creation_form(self):
        response = self.client.get("/tech_support/new/")
        self.assertContains(response, "官署発信情報の登録", status_code=200)
        self.assertTemplateUsed(
            response, "tech_supports/techSupportNewOrEdit.html")

    def test_create_info(self):
        login(self)
        addMockTechSupport(self)
        support = TechSupports.objects.get_or_none(title=self.params['title'])
        if support:
            self.assertEqual(self.params['content'], support.content)
        else:
            self.assertEqual(TechSupports.objects.all().count(), 1)
            self.fail('addressが空')


def edit_common_setUp(testCase, isEdit: bool):
    login(testCase)
    addMockTechSupport(testCase)
    support = TechSupports.objects.get_or_none(title=testCase.params['title'])
    if support:
        if isEdit:
            testCase.response = testCase.client.get(
                "/tech_support/%s/edit/" % support.id)
        else:
            testCase.response = testCase.client.get(
                "/tech_support/%s/" % support.id)
    else:
        testCase.fail('あるはずのMockInfoが見つからない')


class EditSupportTest(TestCase):
    def setUp(self) -> None:
        edit_common_setUp(self, True)

    def test_should_use_expected_template(self):
        self.assertTemplateUsed(
            self.response, "tech_supports/techSupportNewOrEdit.html")


class EditSupportsTest(TestCase):
    def test_should_resolve_support_edit(self):
        found = resolve("/tech_support/1/edit/")
        self.assertEqual(support_edit, found.func)


class SupportDelTest(TestCase):
    def setUp(self) -> None:
        login(self)
        addMockTechSupport(self)

    def test_support_del_count(self):
        support = TechSupports.objects.get_or_none(
            title=self.params['title'])
        if support:
            response = self.client.get(
                "/tech_support/" + str(support.pk) + "/del/")
            self.assertRedirects(
                response, reverse('support_list'), status_code=302,
                target_status_code=200, msg_prefix='',
                fetch_redirect_response=True)
        else:
            self.fail('あるはずのmockが見つからない')

        support = TechSupports.objects.get_or_none(
            title=self.params['title'])
        self.assertIsNone(support)
