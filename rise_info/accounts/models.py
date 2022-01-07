from django.contrib.auth.models import User

def createUser(office):
    if User.objects.filter(username=office.id).count() == 0:
        user = User.objects.create(
            username=office.id,
            first_name=office.name,
            last_name=office.shortcut_name,
        )
        user.set_password(office.id)
        user.save()