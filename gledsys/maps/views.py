from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def lighning_distribution_maps(request):
    context = {
        "page_title": "Lightning Distribution Maps",
    }

    return render(request, 'lightning_distribution.html', context)
