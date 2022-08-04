from django.contrib.auth import get_user_model
from django.test import TestCase

from infos.models import Info, AttachmentFile, InfoTypeChoices, InfoComments

import datetime


class InfoModelTest(TestCase):
    def test_is_empty(self) -> None:
        infos = Info.objects.all()
        self.assertEqual(infos.count(), 0)

    def test_manager_get_or_none_is_get(self):
        user = get_user_model().objects.create_user(
            username='test',
            password='test'
        )
        expected = Info.objects.create(
            title='タイトル',
            info_type=InfoTypeChoices.TECHINICAL,
            managerID='test-00',
            sammary='概要',
            disclosure_date=datetime.date(2017, 11, 12),
            created_by=user,
        )
        actual = Info.objects.get_or_none(pk=expected.pk)
        self.assertEqual(expected, actual)

    def test_manager_get_or_none_is_none(self):
        user = get_user_model().objects.create_user(
            username='test',
            password='test'
        )
        dummy = Info.objects.create(
            title='タイトル',
            info_type=InfoTypeChoices.TECHINICAL,
            managerID='test-00',
            sammary='概要',
            disclosure_date=datetime.date(2017, 11, 12),
            created_by=user,
        )
        actual = Info.objects.get_or_none(pk=dummy.pk + 1)
        self.assertEqual(None, actual)


class AttachmentFileTest(TestCase):
    def test_is_empty(self) -> None:
        attachment = AttachmentFile.objects.all()
        self.assertEqual(attachment.count(), 0)


class InfoCommentTest(TestCase):
    def test_is_empty(self) -> None:
        comment = InfoComments.objects.all()
        self.assertEqual(comment.count(), 0)
