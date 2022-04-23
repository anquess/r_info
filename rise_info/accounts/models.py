from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User


def createUser(offices):
    user_create_object = []
    user_update_object = []
    for office in offices:
        if User.objects.filter(username=office['username']).exists():
            user = User.objects.get(username=office['username'])
            user.first_name = office['first_name']
            user.last_name = office['last_name']
            user.is_active = office['is_active']
            user_update_object.append(user)
        else:
            user_create_object.append(User(
                username=office['username'],
                first_name=office['first_name'],
                last_name=office['last_name'],
                is_active=office['is_active'],
                password=make_password(office['username'])
            ))
    User.objects.bulk_create(user_create_object)
    User.objects.bulk_update(user_update_object, fields=[
                             'first_name', 'last_name'])
