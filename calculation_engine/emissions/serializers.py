from rest_framework import serializers
from .models import Emission


class EmissionFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emission
        fields = '__all__'