from rest_framework import serializers
from .models import NLPmodel

class NLPmodelSerializer(serializers.ModelSerializer):
    class Meta:
        model = NLPmodel
        fields = ['address']