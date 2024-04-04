from django.db import models
from django.urls import reverse

# Create your models here.


class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Person(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)

    gender = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.gender
