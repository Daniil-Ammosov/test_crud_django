import json

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt

from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view

from .models import Person, Apartment
from .serializers import PersonSerializer, ApartmentSerializer


def index(request):
    return HttpResponse("Index page")


class PersonViewSet(ModelViewSet):
    queryset = Person.objects.all().order_by("id")
    serializer_class = PersonSerializer


class ApartmentViewSet(ModelViewSet):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer





# =========================================================================
#                               Views
# =========================================================================
class PersonView(generics.CreateAPIView, generics.ListCreateAPIView, generics.GenericAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    # permission_classes = [IsAdminUser]

    def list(self, request, *args, **kwargs):
        # Note the use of `get_queryset()` instead of `self.queryset`
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return JsonResponse(serializer.data)

    def perform_create(self, request, *args, **kwargs):
        person = get_object_or_404(Person, id=self.request.data.get('name'))
        return self.serializer_class.save(person)


# =========================================================================
#                               PERSON
# =========================================================================
def get_person(request, person_id):
    person = get_object_or_404(Person, id=person_id)
    return JsonResponse(model_to_dict(person))


@csrf_exempt
def create_person(request):
    name = json.loads(request.body.decode("utf-8")).get("name")
    if name and isinstance(name, str):
        new_person = Person.objects.create(name=name)
        return JsonResponse({"msg": f"Person #{new_person.id} is created"})

    return JsonResponse({"msg": "Field 'name' is incorrect"}, status=400)


@csrf_exempt
def update_person(request, person_id):
    if request.method != "PUT":
        return JsonResponse({"msg": "Only 'PUT' methods"}, status=400)

    person = get_object_or_404(Person, id=person_id)
    name = json.loads(request.body.decode("utf-8")).get("name")
    if name is None:
        return JsonResponse({"msg": "Field 'name' is empty"}, status=400)

    person.name = name
    person.save()
    return JsonResponse({"msg": f"Person #{person.id} is updated"})


@csrf_exempt
def delete_person(request, person_id):
    if request.method != "DELETE":
        return JsonResponse({"msg": "Only 'DELETE' methods"}, status=400)

    person = get_object_or_404(Person, id=person_id)
    person.delete()
    return JsonResponse({"msg": f"Person #{person_id} is deleted"})


# =========================================================================
#                               APARTMENT
# =========================================================================
def get_apartment(request, apartment_id):
    apartment = get_object_or_404(Apartment, id=apartment_id)
    return JsonResponse(model_to_dict(apartment))


def get_apartment_list(request):
    data = []
    for each in Apartment.objects.all():
        data.append(model_to_dict(each))

    return JsonResponse({"data": data})


@csrf_exempt
def create_apartment(request):
    if request.method != "POST":
        return JsonResponse({"msg": "Only 'POST' methods"}, status=400)

    input_data = json.loads(request.body.decode("utf-8"))
    if not (input_data.get("address") or input_data.get("furniture") or input_data.get("owner")):
        return JsonResponse({"msg": "Required fields if empty"}, status=400)

    checked_person = get_object_or_404(Person, id=input_data["owner"])
    new_apartment = Apartment.objects.create(owner=checked_person,
                                             address=input_data["address"],
                                             furniture=input_data["furniture"])
    return JsonResponse({"msg": f"Apartment #{new_apartment.id} is created"}, status=400)


@csrf_exempt
def update_apartment(request, apartment_id):
    if request.method != "PUT":
        return JsonResponse({"msg": "Only 'PUT' methods"}, status=400)

    try:
        input_data = json.loads(request.body.decode("utf-8"))
    except json.decoder.JSONDecodeError as e:
        return JsonResponse({"msg": str(e)}, status=400)

    apartment = get_object_or_404(Apartment, id=apartment_id)
    if input_data.get("owner"):
        apartment.owner = get_object_or_404(Person, id=input_data['owner'])
    if input_data.get("address"):
        apartment.address = input_data["address"]
    if input_data.get("furniture"):
        apartment.furniture = input_data["furniture"]

    apartment.save()
    return JsonResponse({"msg": f"Apartment #{apartment.id} is updated"})


@csrf_exempt
def delete_apartment(request, apartment_id):
    if request.method != "DELETE":
        return JsonResponse({"msg": "Only 'DELETE' methods"}, status=400)

    get_object_or_404(Apartment, id=apartment_id).delete()
    return JsonResponse({"msg": f"Apartment #{apartment_id} is deleted"})
