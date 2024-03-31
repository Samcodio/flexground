from django.shortcuts import render, redirect

from .models import Country, Person
from django.urls import reverse
import openai
import os

api_key = "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"

def home(request):
    # print(loader.get_template_dirs())  # Only needed if you're debugging template loading.
    countries = Country.objects.all()
    persons = Person.objects.all()
    context = {'countries': countries, 'persons': persons}
    return render(request, 'take_app/index.html', context)


def get_names(request):
    if request.method == 'GET':
        country = request.GET.get('country')
        gender = request.GET.get('Gender')

        if api_key:
            openai.api_key = api_key
            response = openai.Completion.create(
                engine="gpt-3.5-turbo",
                prompt=f"Generate some {country} names for me, {gender} ones only",
                max_tokens=50
            )

            generated_names = response['choices'][0]['text'].strip()
        else:
            generated_names = "Error: OpenAI API key not found"

        context = {'country': country, 'gender': gender, 'generated_names': generated_names}
        return render(request, 'take_app/names.html', context)

    return render(request, 'take_app/names.html')