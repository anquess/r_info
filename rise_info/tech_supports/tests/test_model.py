from django.test import TestCase

from ..models import TechSupports, TechSupportComments
from ..tests.test_form import make_mock_right_param, mock_tech_support


class TechSupportsModelTest(TestCase):
    def setUp(self) -> None:
        make_mock_right_param(self)
        return super().setUp()

    def test_is_empty(self) -> None:
        sut_instace = TechSupports.objects.all()
        self.assertEqual(sut_instace.count(), 0)

    def test_manager_get_or_none_is_get(self):
        expected = mock_tech_support(self)
        actual = TechSupports.objects.get_or_none(pk=expected.pk)
        self.assertEqual(expected, actual)
        actual = TechSupports.objects.get_or_none(pk=expected.pk + 1)
        self.assertEqual(None, actual)
        try:
            expected.eqtypes.set(self.params['eqtypes'])
        except:
            self.fail('manytomany Error')
