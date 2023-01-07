from django.test import TestCase

from contents.views import addMenus
from contents.models import ContentsRelation
from contents.tests.test_model import mock_menu, mock_content
from accounts.tests.com_setup import login


def addMockContent(testCase):
    login(testCase)
    mock_menu(testCase)
    params_1_1 = {"title": 'title1_1', "menu": testCase.menu_1}
    params_1_2 = {"title": 'title1_2', "menu": testCase.menu_1}
    params_2_1 = {"title": 'title2_1', "menu": testCase.menu_2}
    params_2_2 = {"title": 'title2_2', "menu": testCase.menu_2}
    testCase.client.post("contents/new/?menu=" +
                         str(testCase.menu_1.id), params_1_1)
    testCase.client.post("contents/new/?menu=" +
                         str(testCase.menu_1.id), params_1_2)
    testCase.client.post("contents/new/?menu=" +
                         str(testCase.menu_2.id), params_2_1)
    testCase.client.post("contents/new/?menu=" +
                         str(testCase.menu_2.id), params_2_2)

    testCase.content_1_1 = ContentsRelation.objects.get_or_none(
        title='title1_1')
    testCase.content_1_2 = ContentsRelation.objects.get_or_none(
        title='title1_2')
    testCase.content_2_1 = ContentsRelation.objects.get_or_none(
        title='title2_1')
    testCase.content_2_2 = ContentsRelation.objects.get_or_none(
        title='title2_2')
    return testCase


class MenuViewTest(TestCase):
    def setUp(self) -> None:
        mock_menu(self)
        login(self)

    def test_add_menus(self) -> None:
        context = {}
        context = addMenus(context)
        self.assertEqual(context['menus'][0], self.menu_1)
        self.assertEqual(context['menus'][1], self.menu_2)

    def test_menu_down(self) -> None:
        response = self.client.get(
            "/contents/menu/down/" + str(self.menu_1.pk) + "/")
        self.assertRedirects(response, '/contents/menu/list/',
                             status_code=302, msg_prefix='メニューを動かしました')

    def test_menu_down_not(self) -> None:
        response = self.client.get(
            "/contents/menu/down/" + str(self.menu_2.pk) + "/")
        self.assertRedirects(response, '/contents/menu/list/',
                             status_code=302, msg_prefix='これより上はありません')

    def test_menu_up(self) -> None:
        response = self.client.get(
            "/contents/menu/up/" + str(self.menu_2.pk) + "/")
        self.assertRedirects(response, '/contents/menu/list/',
                             status_code=302, msg_prefix='メニューを動かしました')

    def test_menu_up_not(self) -> None:
        response = self.client.get(
            "/contents/menu/up/" + str(self.menu_1.pk) + "/")
        self.assertRedirects(response, '/contents/menu/list/',
                             status_code=302, msg_prefix='これより上はありません')

    def test_menu_list_retun_200_include_menu_contents(self) -> None:
        response = self.client.get("/contents/menu/list/")
        self.assertContains(response, self.menu_1.menu_title, status_code=200)

    def test_menu_list_uses_expected_template(self) -> None:
        response = self.client.get("/contents/menu/list/")
        self.assertTemplateUsed(response, "contents/menu_list.html")


class ContentsViewTest(TestCase):
    def setUp(self) -> None:
        user = login(self)
        mock_content(self, user)
        addMockContent(self)

    def test_contents_detail_return_200_and_include_title(self) -> None:
        response = self.client.get(
            '/contents/' + str(self.content_1_1.id) + '/')
        self.assertContains(response, self.content_1_1.title, status_code=200)

    def test_contents_detail_uses_expected_template(self) -> None:
        response = self.client.get(
            '/contents/' + str(self.content_1_1.id) + '/')
        self.assertTemplateUsed(response, "contents/content_detail.html")

    def test_contents_new_return_200_and_include_title(self):
        response = self.client.get(
            "/contents/new/?menu=" + str(self.menu_1.id))
        self.assertContains(response, "Wikiの登録", status_code=200)

    def test_contents_new_uses_expected_template(self):
        response = self.client.get(
            "/contents/new/?menu=" + str(self.menu_1.id))
        self.assertTemplateUsed(response, "contents/contentNewOrEdit.html")

    def test_contents_edit_return_200_and_include_title(self) -> None:
        response = self.client.get(
            '/contents/' + str(self.content_1_1.id) + '/edit/')
        self.assertContains(response, self.content_1_1.title, status_code=200)

    def test_contents_edit_uses_expected_template(self) -> None:
        response = self.client.get(
            '/contents/' + str(self.content_1_1.id) + '/edit/')
        self.assertTemplateUsed(response, "contents/contentNewOrEdit.html")

    def test_content_down(self) -> None:
        response = self.client.get(
            "/contents/content/down/" + str(self.content_1_1.pk) + "/")
        self.assertRedirects(response, '/contents/menu/list/',
                             status_code=302, msg_prefix='メニューを動かしました')

    def test_content_down_not(self) -> None:
        response = self.client.get(
            "/contents/content/down/" + str(self.content_1_2.pk) + "/")
        self.assertRedirects(response, '/contents/menu/list/',
                             status_code=302, msg_prefix='これより上はありません')

    def test_content_up(self) -> None:
        response = self.client.get(
            "/contents/content/up/" + str(self.content_1_2.pk) + "/")
        self.assertRedirects(response, '/contents/menu/list/',
                             status_code=302, msg_prefix='メニューを動かしました')

    def test_content_up_not(self) -> None:
        response = self.client.get(
            "/contents/content/up/" + str(self.content_1_1.pk) + "/")
        self.assertRedirects(response, '/contents/menu/list/',
                             status_code=302, msg_prefix='これより上はありません')
