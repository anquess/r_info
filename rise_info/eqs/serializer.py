from django.db import models
from rest_framework import fields, serializers
from .models import Eqtype

class EqtypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eqtype
        fields = ('id',)