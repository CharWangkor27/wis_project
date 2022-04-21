from itertools import product
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product
# Create your views here.


def sayhello(request):
    return render(request, 'home.html')
