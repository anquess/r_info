from django.contrib.auth.models import User

def createUser(office):
    if User.objects.filter(username=office.slug).count() == 0:
        User.objects.create(
            username=office.slug,
            password=office.slug,
            first_name=office.name,
            last_name=office.shortcut_name,
        )