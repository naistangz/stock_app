from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
import requests
import json


from .models import *
from .forms import *


def home(request):

    if request.method == "POST":
        symbol = request.POST['symbol']
        try:
            api_request = requests.get(
                f'https://cloud.iexapis.com/stable/stock/{symbol}/quote?token={settings.API_KEY}'
            )
            api = json.loads(api_request.content)
        except Exception as e:
            print(e)
            api = 'Error...'
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        return render(request, 'home.html', {'api': api})
    else:
        return render(request, 'home.html', {'symbol': 'Enter a ticker symbol'})


def add_stock(request):
    if request.method == 'POST':
        form = StockForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(
                request, u'Stock has been added successfully! \U0001f600')
            return redirect(add_stock)

    else:
        symbols = Stock.objects.all()

        output = []

        for item in symbols:
            try:
                api_request = requests.get(
                    f'https://cloud.iexapis.com/stable/stock/{item}/quote?token={settings.API_KEY}'
                )
                api = json.loads(api_request.content)
                output.append(api)
            except Exception as e:
                messages.error(
                    request, f'Unable to find data for {item} \U0001F61E'
                )

        return render(request, 'add_stock.html', {
            'symbols': symbols,
            'output': output
        })


def delete(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, f'The ticker {item} has been deleted \U0001f600')
    return redirect(delete_stock)


def delete_stock(request):
    symbols = Stock.objects.all()

    return render(request, 'delete_stock.html', {'symbols': symbols})


def about(request):
    return render(request, 'about.html', {})
