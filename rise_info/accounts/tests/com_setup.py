from django.contrib.auth.models import Group, User

# Create your tests here.


def testTMCAcountCreate(testCase):
    testCase.user = User.objects.create(
        username="test_user",
        password="top_secret_pass0001",
        is_staff=True,
    )


def testAcountCreate(testCase):
    testCase.user = User.objects.create(
        username="test_user2",
        password="top_secret_pass0002",
    )


def rootAcountCreate(testCase):
    testCase.user = User.objects.create(
        username="root",
        password="root_secret_pass0001",
        is_staff=True,
    )


def login(testCase):
    if not hasattr(testCase, 'user'):
        testTMCAcountCreate(testCase)
    testCase.client.force_login(testCase.user)
    return testCase.user


def loginTestAccount(testCase) -> None:
    if not hasattr(testCase, 'user'):
        testAcountCreate(testCase)
    testCase.client.force_login(testCase.user)


def addMockUser(testCase) -> None:
    testCase.client.force_login(testCase.user)
    data = {
        'username': testCase.username,
        'password1': testCase.password,
        'password2': testCase.password,
    }
    testCase.response = testCase.client.post("/accounts/new/", data)
