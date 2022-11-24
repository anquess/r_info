from django.test import TestCase, tag
from django.contrib.auth.models import User

from datetime import datetime as dt
import pytz
import random
import string

from ..models import Eqtype

mock_update_at = dt(2019, 7, 15, 15, 22, 48, 0, pytz.timezone('Asia/Tokyo'))


def randomname(length, charactors=string.ascii_letters + string.digits):
    randlst = [random.choice(charactors) for i in range(length)]
    return ''.join(randlst)


def make_mock_eqtypes(grp=None):
    random_slag_24 = randomname(
        18, string.ascii_uppercase) + randomname(6, string.digits)
    eqtype = Eqtype.objects.create(
        id=random_slag_24,
        slug=random_slag_24,
        create_at=mock_update_at,
    )
    return eqtype
