from django.contrib import admin
from .models import Person, Country, CustomUser


admin.site.register(Country)
admin.site.register(Person)


admin.site.register(CustomUser)
