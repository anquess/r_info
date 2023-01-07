from django.test import TestCase

from accounts.tests.com_setup import login
from contents.models import ContentsRelation, Menu  # , ContentComments


def mock_menu(testCase: TestCase):
    testCase.menu_1 = Menu(menu_title='title1')
    testCase.menu_2 = Menu(menu_title='title2')
    testCase.menu_1.create()
    testCase.menu_2.create()
    return testCase


def mock_content(testCase: TestCase, user):
    testCase = mock_menu(testCase)
    testCase.content_1_1 = ContentsRelation.objects.create(
        title='title1_1', menu=testCase.menu_1, created_by=user)
    testCase.content_1_2 = ContentsRelation.objects.create(
        title='title1_2', menu=testCase.menu_1, created_by=user)
    testCase.content_2_1 = ContentsRelation.objects.create(
        title='title2_1', menu=testCase.menu_2, created_by=user)
    testCase.content_2_2 = ContentsRelation.objects.create(
        title='title2_2', menu=testCase.menu_2, created_by=user)
    return testCase


class MenuModelTest(TestCase):
    def setUp(self) -> None:
        mock_menu(self)

    def test_menu_create(self):
        menus = Menu.objects.all()
        self.assertEqual(len(menus), 2)
        self.assertEqual(menus[0].menu_title, 'title1')
        self.assertEqual(menus[0].sort_num, 1)
        self.assertEqual(menus[1].menu_title, 'title2')
        self.assertEqual(menus[1].sort_num, 2)

    def test_menu_replace_sort_num(self):
        menus = Menu.objects.all()
        menus[0].replace_sort_num(menus[1])
        self.assertEqual(menus[0].menu_title, 'title1')
        self.assertEqual(menus[0].sort_num, 2)
        self.assertEqual(menus[1].menu_title, 'title2')
        self.assertEqual(menus[1].sort_num, 1)


class ContensModelTest(TestCase):
    def test_is_empty(self) -> None:
        contents = ContentsRelation.objects.all()
        self.assertEqual(contents.count(), 0)

    def test_contents_create(self):
        user = login(self)
        mock_content(self, user)
        contents = ContentsRelation.objects.all()
        self.assertEqual(contents.count(), 4)

    def test_contents_replace_sort_num(self):
        user = login(self)
        mock_content(self, user)
        contents = ContentsRelation.objects.all()
        contents[0].replace_sort_num(contents[1])
        self.assertEqual(contents[0].title, 'title1_1')
        self.assertEqual(contents[0].sort_num, 2)
        self.assertEqual(contents[1].title, 'title1_2')
        self.assertEqual(contents[1].sort_num, 1)


# class ContentsCommentTest(TestCase):
#    def test_is_empty(self) -> None:
#        comment = ContentComments.objects.all()
#        self.assertEqual(comment.count(), 0)
