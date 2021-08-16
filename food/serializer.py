from rest_framework import serializers

from .models import Fruit, Vegetable


class FruitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fruit
        fields = ('name',)


class VegetableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vegetable
        fields = ('name',)
