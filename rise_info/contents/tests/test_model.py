from django.test import TestCase

from contents.models import Contents, Menu


def mock_menu(testCase: TestCase):
    testCase.menu_1 = Menu.objects.create(menu_title='title1')
    testCase.menu_2 = Menu.objects.create(menu_title='title2')
    return testCase


def mock_content(testCase: TestCase):
    testCase = mock_menu(testCase)
    testCase.content_1_1 = Contents.objects.create(
        title='title1_1', menu=testCase.menu_1)
    testCase.content_1_2 = Contents.objects.create(
        title='title1_2', menu=testCase.menu_1)
    testCase.content_2_1 = Contents.objects.create(
        title='title2_1', menu=testCase.menu_2)
    testCase.content_2_2 = Contents.objects.create(
        title='title2_2', menu=testCase.menu_2)
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
        contents = Contents.objects.all()
        self.assertEqual(contents.count(), 0)

    def test_contents_create(self):
        mock_content(self)
        contents = Contents.objects.all()
        self.assertEqual(contents.count(), 4)

    def test_contents_replace_sort_num(self):
        mock_content(self)
        contents = Contents.objects.all()
        contents[0].replace_sort_num(contents[1])
        self.assertEqual(contents[0].title, 'title1_1')
        self.assertEqual(contents[0].sort_num, 2)
        self.assertEqual(contents[1].title, 'title1_2')
        self.assertEqual(contents[1].sort_num, 1)
