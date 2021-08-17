from rest_framework import serializers

from .models import Person, Apartment


class ApartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apartment
        fields = "__all__"


class PersonSerializer(serializers.ModelSerializer):
    apartments = ApartmentSerializer(read_only=True, many=True)

    class Meta:
        model = Person
        fields = "__all__"
