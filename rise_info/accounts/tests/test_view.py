from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.shortcuts import get_object_or_404

from accounts.tests.com_setup import testAcountCreate, login, rootAcountCreate, addMockUser, testTMCAcountCreate


class WithoutRootLoginAccountNewPageTest(TestCase):
    def test_without_login_new_return_302(self):
        response = self.client.get("/accounts/new/")
        self.assertEqual(response.status_code, 302)

    def test_not_allow_login_return_404(self):
        testAcountCreate(self)
        login(self)
        response = self.client.get("/accounts/new/")
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'この権限では登録は許可されていません。')


class WithRootLoginAccountNewPageTest(TestCase):
    def setUp(self) -> None:
        rootAcountCreate(self)
        login(self)
        return super().setUp()

    def test_new_return_200_and_expected_title(self) -> None:
        response = self.client.get("/accounts/new/")
        self.assertContains(response, "ユーザー登録", status_code=200)

    def test_new_uses_expected_template(self):
        response = self.client.get("/accounts/new/")
        self.assertTemplateUsed(response, "accounts/account_new.html")

    def test_create_account_login(self):
        self.username = "test_user2",
        self.password = "top_secret_pass0002",
        addMockUser(self)
        self.assertEqual(self.response.status_code, 302)
        self.assertEqual(User.objects.all().count(), 2)
        self.user = User.objects.all().get(username="test_user2")
        login(self)
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/accounts/new/")
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'この権限では登録は許可されていません。')


class AccountListTest(TestCase):
    def setUp(self) -> None:
        rootAcountCreate(self)
        login(self)
        return super().setUp()

    def test_account_list_return_200_and_expected_title(self) -> None:
        response = self.client.get("/accounts/")
        self.assertContains(response, "ユーザー一覧", status_code=200)

    def test_account_list_uses_expected_template(self) -> None:
        response = self.client.get("/accounts/")
        self.assertTemplateUsed(response, "accounts/account_list.html")


class PassWordChangeTest(TestCase):
    def setUp(self) -> None:
        testTMCAcountCreate(self)
        login(self)
        return super().setUp()

    def test_password_change_use_expected_template(self) -> None:
        response = self.client.get("/accounts/password_change/")
        self.assertTemplateUsed(response, "accounts/password_change.html")

    def test_password_change_not_NewPW(self) -> None:
        data = {
            'old_password': self.user.password,
            'new_password1': 'mjk2r7h4u5',
            'new_password2': 'mjk2r',
        }
        response = self.client.post("/accounts/password_change/", data)
        self.assertContains(response, "確認用パスワードが一致しません。", status_code=200)

    def test_password_change_not_oldPW(self) -> None:
        data = {
            'old_password': 'mjk2r7h4u5',
            'new_password1': 'mjk2r7h4u5',
            'new_password2': 'mjk2r7h4u5',
        }
        response = self.client.post("/accounts/password_change/", data)
        self.assertContains(response, "元のパスワードが間違っています。", status_code=200)


class UserDelTest(TestCase):
    def setUp(self) -> None:
        testAcountCreate(self)
        rootAcountCreate(self)
        login(self)
        return super().setUp()

    def test_del_test_Acount(self) -> None:
        pk = get_object_or_404(User, username="test_user2").pk
        response = self.client.get("/accounts/" + str(pk) + "/del/")
        self.assertNotContains(response, "test_user2", status_code=302)
