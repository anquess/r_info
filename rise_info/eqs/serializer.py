from rest_framework import serializers
from .models import Eqtype


class EqtypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eqtype
        fields = ('id',)
