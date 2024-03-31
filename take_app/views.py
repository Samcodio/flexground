from django.shortcuts import render, redirect

from .models import Country, Person
from django.urls import reverse
import openai , os

api_key = ""

def home(request):
    # print(loader.get_template_dirs())  # Only needed if you're debugging template loading.
    countries = Country.objects.all()
    persons = Person.objects.all()
    context = {'countries': countries, 'persons': persons}
    return render(request, 'take_app/index.html', context)


def get_names(request):
    if request.method == 'GET':

        country = request.POST.get('country')
        gender = request.POST.get('Gender')
        if country == "" and gender == "":
            return redirect(request,'take_app/index.html')
        else:
            print(gender,country)
            if api_key:
                openai.api_key = api_key
                response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=f"Generate some {country} names for me, {gender} ones only",
                    max_tokens=50
                )

                generated_names = response.choices[0].text.strip()
            else:
                generated_names = "Error: OpenAI API key not found"

            context = {'country': country, 'gender': gender, 'generated_names': generated_names}
        return render(request, 'take_app/names.html', context)

    return render(request, 'take_app/names.html')
