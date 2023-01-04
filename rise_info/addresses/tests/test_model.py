from django.test import TestCase

from addresses.models import Addresses
from ..tests.test_form import make_mock_right_param


class AddresseModelTest(TestCase):
    def setUp(self) -> None:
        make_mock_right_param(self)
        return super().setUp()

    def test_is_empty(self) -> None:
        addresses = Addresses.objects.all()
        self.assertEqual(addresses.count(), 0)

    def test_manager_get_or_none_is_get(self):
        expected = Addresses.objects.create(
            name=self.params['name'],
            position=self.params['position'],
            mail=self.params['mail'],
        )
        actual = Addresses.objects.get_or_none(pk=expected.pk)
        self.assertEqual(expected, actual)
        actual = Addresses.objects.get_or_none(pk=expected.pk + 1)
        self.assertEqual(None, actual)
