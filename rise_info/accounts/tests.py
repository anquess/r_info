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
