from rest_framework.serializers import HyperlinkedModelSerializer, ModelSerializer, RelatedField

from .models import Person, Apartment


class OwnerField(RelatedField):
    def to_representation(self, model_instance):
        return {"name": model_instance.name, "id": model_instance.id}


class ApartmentSerializer(ModelSerializer):
    owner = OwnerField(read_only=True)

    class Meta:
        model = Apartment
        fields = "__all__"


class ApartmentWithoutOwnerSerializer(ModelSerializer):

    class Meta:
        model = Apartment
        exclude = ["owner"]


class PersonSerializer(HyperlinkedModelSerializer):
    apartments = ApartmentWithoutOwnerSerializer(many=True, read_only=True)

    class Meta:
        model = Person
        fields = ["id", "name", "url", "apartments"]
