from json import loads

from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.generics import ListAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.views import APIView

from .models import Person, Apartment
from .serializers import PersonSerializer, ApartmentSerializer


def index(request):
    return HttpResponse("Index page")


class PersonList(ListAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = (IsAuthenticated,)


class PersonDetail(APIView):
    model = Person
    serializer = PersonSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        return get_object_or_404(self.model, pk=pk)

    def get(self, request, pk):
        instance = get_object_or_404(self.model, pk=pk)
        serializer = self.serializer(instance)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(status=HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        serializer = self.serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.update(self.get_object(pk), serializer.data)
            return Response(f"{self.model.__name__} #{pk} was changed")

        return Response(status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        get_object_or_404(self.model, pk=pk).delete()
        return Response(f"{self.model.__name__} #{pk} was deleted")


class ApartmentList(ListAPIView):
    serializer_class = ApartmentSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        try:
            address = loads(self.request.query_params.get("address"))
        except TypeError:
            address = None

        try:
            furniture = loads(self.request.query_params.get("furniture"))
        except TypeError:
            furniture = None

        owner = self.request.query_params.get("owner")

        queryset = Apartment.objects.all()
        if address is not None:
            queryset = queryset.filter(address__exact=address)
        if furniture is not None:
            queryset = queryset.filter(furniture__exact=furniture)
        if owner is not None:
            queryset = queryset.filter(owner__name__contains=owner)

        return queryset


class ApartmentDetail(PersonDetail, UpdateModelMixin):
    model = Apartment
    serializer = ApartmentSerializer

    def patch(self, request, pk):
        serializer = self.serializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.update(self.get_object(pk), serializer.initial_data)
            return Response(f"{self.model.__name__} #{pk} was changed")

        return Response(status=HTTP_400_BAD_REQUEST)
