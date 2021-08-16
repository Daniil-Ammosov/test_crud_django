from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Apartment(models.Model):
    owner = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='apartments')
    address = models.JSONField()
    furniture = models.JSONField()

    def __str__(self):
        return f"Owner:{self.owner.name}; Address:{self.address}"
