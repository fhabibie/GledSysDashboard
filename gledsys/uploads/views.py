from http.client import HTTPResponse
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def index(request):
    context = {
        'name': 'Hello',
        'page_title': 'Dashboard',
    }
    return render(request, 'dashboard.html', context)