from rest_framework import serializers
from .models import *

class RubricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rubric
        fields = ['id', 'name']


class AdSerializer(serializers.ModelSerializer):
    rubric = RubricSerializer()
    class Meta:
        model = Ad
        fields = ['id', 'rubric', 'title', 'price', 'content']