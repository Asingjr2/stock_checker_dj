import time
from django.views import View
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import date, datetime, timedelta
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404

import requests

from .models import Stock
from .forms import StockCreateForm


# Create your views here.
class RefreshAllStocks(LoginRequiredMixin, View):
    def get(self, request):
        user_stocks = Stock.objects.all().filter(user__id=self.request.user.id)
        today = datetime.today()
        subtract_day = timedelta(days=-1)
        substract_two_days = timedelta(days=-2)

        if today.strftime("%A") == "Saturday":
            today += subtract_day
        if today.strftime("%A") == "Sunday":
            today += substract_two_days
        
        # Format used in JSON response
        today_formatted = today.strftime("%Y-%m-%d")

        for stock in user_stocks:
            url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + str(stock.ticker_symbol) + "&apikey=HVS4381TKE7Y9YOS"
            resp = requests.get(url).json()['Time Series (Daily)'][today_formatted]
            stock.s_open = round(float(resp["1. open"]),2)
            stock.s_close = round(float(resp["4. close"]),2)
            stock.s_high = round(float(resp["2. high"]),2)
            stock.s_low = round(float(resp["3. low"]),2)
            stock.save()

        return redirect("/stocks/home/")


class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        queryset = Stock.objects.all().filter(user__id = (self.request.user.id))
        if "current_stock" in request.session:
            # Delete current stock saved from stock query
            del request.session["current_stock"]
            request.session.modified = True

        return render(request, "stocks/home.html", {"user_stocks": queryset, "ff": StockCreateForm})


class StockSearchView(LoginRequiredMixin, View):
    def get(self, request):
        if "current_stock" in request.session:
            subtract_day = timedelta(days=-1)
            substract_two_days = timedelta(days=-2)
            today = datetime.today()
            current_time = datetime.now()

            # Altering time to cover cases where stock market is closed (i.e. Saturday, Sunday, before 9:30 AM EST).  Holidays closures not addressed below.
            if int(current_time.strftime("%H")) < 9 and int(current_time.strftime("%M")) < 31:
                today += subtract_day
            if today.strftime("%A") == "Saturday":
                today += subtract_day
            if today.strftime("%A") == "Sunday":
                today += substract_two_days

            today_formatted = today.strftime("%Y-%m-%d")

            response = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + str(request.session["current_stock"]) + "&apikey=HVS4381TKE7Y9YOS")
            if 'Time Series (Daily)' in response.json():
                ss = response.json()['Time Series (Daily)'][today_formatted]
                day_open = round(float(ss["1. open"]),2)
                day_high = round(float(ss["2. high"]),2)
                day_low = round(float(ss["3. low"]),2)
                day_close = round(float(ss["4. close"]),2)
                context = {
                    "symbol" : request.session["current_stock"],
                    "day_open": day_open,
                    "day_close": day_close, 
                    "day_high": day_high,
                    "day_low": day_low,
                }

                return render(request, "stocks/stock_search.html", context)
            else:
                # HTML page being displayed in api returns no stock data
                return render(request, "stocks/bad_search.html")
        else:
            # HTML page for initial search
            return render(request, "stocks/empty_search.html")

    # Post method to display stock data before user commits to adding to favorites
    def post(self, request):
        new_stock = request.POST["ticker"].upper()
        request.session["current_stock"] = new_stock
        return redirect("/stocks/stock_search/")
