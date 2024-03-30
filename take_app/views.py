from django.shortcuts import render

from  .models import Country, Person


# The loader import can be removed if you're not using it directly in your views.
# from django.template import loader

# This is a view function.
def home(request):
    # print(loader.get_template_dirs())  # Only needed if you're debugging template loading.
    countries = Country.objects.all()
    persons = Person.objects.all()
    context = {'countries': countries, 'persons': persons}
    return render(request, 'take_app/index.html', context)
