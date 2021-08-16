from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"persons", views.PersonViewSet)
router.register(r"apartments", views.ApartmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
