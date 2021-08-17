from django.urls import path, include

from . import views

urlpatterns = [
    path("persons/", views.PersonList.as_view()),
    path("person/", include([
        path("", views.PersonDetail.as_view()),
        path("<pk>/", views.PersonDetail.as_view()),
    ])),

    path("apartments/", views.ApartmentList.as_view()),
    path("apartment/", include([
        path("", views.ApartmentDetail.as_view()),
        path("<pk>/", views.ApartmentDetail.as_view()),
    ])),
]
