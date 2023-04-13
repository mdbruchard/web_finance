from django.shortcuts import render

from bs4 import BeautifulSoup
import requests


# Create your views here.


def index(request):
    return render(request, 'finance/index.html')