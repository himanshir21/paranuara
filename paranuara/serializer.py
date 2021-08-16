from rest_framework import serializers

from food.serializer import FruitSerializer, VegetableSerializer
from .models import Company, People


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('name',)


class PeopleSerializer(serializers.ModelSerializer):
    friends = serializers.SerializerMethodField()
    vegetables = serializers.SerializerMethodField()
    fruits = serializers.SerializerMethodField()

    class Meta:
        model = People
        fields = ('index', 'company', 'name', 'has_died', 'balance', 'picture',
                  'age', 'eyeColor', 'gender', 'email', 'phone', 'address',
                  'about', 'registered', 'greeting', 'tags', 'friends',
                  'vegetables', 'fruits')

    def get_vegetables(self, people):
        return People.objects.filter(index=people.index).values_list(
            'vegetable__name', flat=True)

    def get_fruits(self, people):
        return People.objects.filter(index=people.index).values_list(
            'fruit__name', flat=True)

    def get_friends(self, people):
        return People.objects.filter(index=people.index).values_list(
            'friend__name', flat=True)


class CommonFriendSerializer(serializers.Serializer):
    friends = serializers.ListField(child=serializers.CharField())
    people_one = serializers.JSONField()
    people_two = serializers.JSONField()
