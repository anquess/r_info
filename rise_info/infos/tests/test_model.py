from django.test import TestCase
from infos.models import Info

class InfoModelTest(TestCase):
    def test_is_empty(self) -> None:
        infos = Info.objects.all()
        self.assertEqual(infos.count(), 0)

