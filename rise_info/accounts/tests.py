from django.test import TestCase
from django.contrib.auth.models import Group, User

# Create your tests here.
def testAcountCreate(testCase):
    testCase.user = User.objects.create(
        username="test_user",
        password="top_secret_pass0001",
    )
    group=Group.objects.create(name="TMC")
    group.user_set.add(testCase.user)

def rootAcountCreate(testCase):
    testCase.user = User.objects.create(
        username="root",
        password="root_secret_pass0001",
    )

def login(testCase) -> None:
    if not hasattr(testCase, 'user'):
        testAcountCreate(testCase)
    testCase.client.force_login(testCase.user)

class SignupPageTest(TestCase):
    def test_signup_return_200_and_expected_title(self) -> None:
        rootAcountCreate(self)
        login(self)
        response = self.client.get("/accounts/signup/")
        self.assertContains(response,"信頼性情報" , status_code=200)

    def test_signup_uses_expected_template(self):
        rootAcountCreate(self)
        login(self)
        response = self.client.get("/accounts/signup/")
        self.assertTemplateUsed(response, "accounts/signup.html")

    def test_without_login_signup__return_302(self):
        response = self.client.get("/accounts/signup/")
        self.assertEqual(response.status_code, 302)