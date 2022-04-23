from django.test import TestCase

from ..models import FailuerReport


class InfoModelTest(TestCase):
    def test_is_empty(self) -> None:
        infos = FailuerReport.objects.all()
        self.assertEqual(infos.count(), 0)
