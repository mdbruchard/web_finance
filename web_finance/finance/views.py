from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from bs4 import BeautifulSoup
import requests


# Create your views here.

def index(request):

    # If request method is POST
    if request.method == 'POST':

        # Saving the request post
        syb1 = request.POST['syb1']
        syb2 = request.POST['syb2']

        # Check if there's no null values or spaces
        if syb1:
            if syb1.isalpha() == False:
                return render(request, 'finance/index.html', {
                    'message': 'You need to fill it up with symbols'
                })
            # If looking for USD to some currency, use only one symbol
            if 'USD' in syb1.upper():
                syb2 = syb2.strip()
                syb2 = syb2.upper()
                symbol = syb2

                return HttpResponseRedirect(reverse('symbol', args=[symbol]))
        else:
            return HttpResponseRedirect(reverse('index'))
        

        if syb2:
            if syb2.isalpha == False:
                return render(request, 'finance/index.html', {
                    'message': 'You need to fill it up with symbols'
                })
        else:
            return HttpResponseRedirect(reverse('index'))
        
        # Remove all the spaces and turn into uppercase
        syb1, syb2 = syb1.strip(), syb2.strip()
        
        syb1, syb2 = syb1.upper(), syb2.upper()
        symbol = syb1 + syb2

        return HttpResponseRedirect(reverse('symbol', args=[symbol]))

    return render(request, 'finance/index.html')

def symbol(request, symbol):
    # Save yahoo link to be scraped
    url = f'https://uk.finance.yahoo.com/quote/{symbol}%3DX'

    r = requests.get(url)

    if str(r.status_code).startswith('2') == False:
        return HttpResponse(
            "<h1 style='text-align: center; margin-top: 25%;'>Sorry, server is down.</h1>", 
            status=404)
    
    sp = BeautifulSoup(r.content, 'html.parser')

    # Scraping all the information
    name = sp.find('h1', {'class': 'D(ib) Fz(18px)'}).text
    
    value = sp.find('fin-streamer', {'class': 'Fw(b) Fz(36px) Mb(-4px) D(ib)'}).text
    
    change = sp.find_all(
        'fin-streamer', {'class': 'Fw(500) Pstart(8px) Fz(24px)'})[0].find('span').text
    
    change_percent = sp.find_all(
        'fin-streamer', {'class': 'Fw(500) Pstart(8px) Fz(24px)'})[1].find('span').text

    # Cleaning the percentage
    percent = change_percent.strip('(%)')



    return render(request, 'finance/symbol.html', {
        'symbol': symbol, 
        'name': name,
        'value': float(value),
        'change': float(change),
        'change_percent': float(percent)
    })
