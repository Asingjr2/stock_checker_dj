import time
from django.views import View
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import date, datetime, timedelta
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404

import requests

from .models import Stock


# Create your views here.
class HomeView(View):
    def get(self, request):
        queryset = Stock.objects.all().filter(user__id = (self.request.user.id))
        stock_data = {}

        today= datetime.today()
        subtract_day = timedelta(days=-1)   
        substract_two_days = timedelta(days=-2)   
        if today.strftime("%A") == "Saturday":
            today += subtract_day
        if today.strftime("%A") == "Sunday":
            today += substract_two_days
        today_formatted = today.strftime("%Y-%m-%d")

        for stock in queryset:
            resp = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + str(stock.ticker_symbol) + "&apikey=HVS4381TKE7Y9YOS")
            data = resp.json()


            if  today_formatted not in data['Time Series (Daily)']:
                print("subtracting a day")
                today += subtract_day
                today_formatted = today.strftime("%Y-%m-%d")
                s_data = resp.json()['Time Series (Daily)'][today_formatted]
                price_data= [ resp.json()["Meta Data"]["2. Symbol"], s_data["1. open"], s_data["2. high"], s_data["3. low"], s_data["4. close"]  ]
                stock_data[str(stock.ticker_symbol)] = price_data
                print(stock_data)

        return render(request, "stocks/home.html", {"user_stocks": queryset, "stock_data": stock_data})


class StockSearchView(View):
    def get(self, request):
        if "current_stock" in request.session:
            subtract_day = timedelta(days=-1)   # Will subtract day if calendar day falls on Sat
            substract_two_days = timedelta(days=-2)   # Will subtract day if calendar day falls on Su
            today = datetime.today()
            
            if today.strftime("%A") == "Saturday":
                today += subtract_day
            if today.strftime("%A") == "Sunday":
                today += substract_two_days

            today_formatted = today.strftime("%Y-%m-%d")


            response = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + str(request.session["current_stock"]) + "&apikey=HVS4381TKE7Y9YOS")
            print("response info {}".format(response))
            print("****")
            if 'Time Series (Daily)' in response.json():
                print("real stock")
                print(response.json()["Meta Data"]["2. Symbol"])
                if  today_formatted not in response.json()['Time Series (Daily)']:
                    print("subtracting a day")
                    today += subtract_day
                    today_formatted = today.strftime("%Y-%m-%d")
                ss = response.json()['Time Series (Daily)'][today_formatted]
                stock_data = [ response.json()["Meta Data"]["2. Symbol"],ss["1. open"], ss["2. high"], ss["3. low"], ss["4. close"]  ]
                print("stock_data info {}".format(stock_data))
                context = {
                    "symbol" : request.session["current_stock"],
                    "stock_data": stock_data,
                    "stock": request.session["current_stock"]
                }
                return render(request, "stocks/stock_search.html", context)
            else:
                print("not real stock")
                messages.warning(request, "SOMETHING EXOTIC")
                return render(request, "stocks/stock_search.html")
                
            # return render(request, "stocks/stock_search.html")
        else:
            print("there is a no stock")
            return render(request, "stocks/stock_search.html")


    def post(self, request):
        new_stock = request.POST["ticker"].upper()
        request.session["current_stock"] = new_stock
        print(request.session["current_stock"])
        if Stock.objects.all().filter(ticker_symbol = new_stock):
            print("there was a match", new_stock)
        print("there was  not a match")
        return redirect("/stocks/stock_search/")


























        # if request.POST["form"] == "new_stock":
        #     # return reverse('stocks:home')
        #     return redirect("/stocks/stock_check/")
        
        # May need to revise
        # if request.POST["form"] == "new_favorite":
        #     request.session["current_ticker"] = request.POST["ticker"]
        #     if Stock.objects.get(name = request.POST["stock"]):
        #         new_favorite_stock = Favorites.objects.create(
        #         stock = Stock.objects.last(),
        #         user = User.objects.get(username = request.user.username)
        #         )
        #     else:
        #         new_stock = Stock.objects.create(
        #             ticker_symbol = request.POST["stock"]
        #         )
        #         new_stock.save()
        #         new_favorite_stock = Favorites.objects.create(
        #             stock = Stock.objects.last(),
        #             user = User.objects.get(username = request.user.username)
        #         )
        #         new_favorite_stock.save()
        #     # return reverse('stocks:home')
        #     return redirect("/stocks/home/")


class StockListView(ListView):
    model = Stock


class StockDetailView(DetailView):
    model = Stock
    pk_url_kwarg = 'stock_id'


class UserDetailView(DetailView):
    model = User

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))


class UserProfileView(View):
    
    def get(self, request):
        user= User.objects.get(username = request.user.username)
        context = {}
        
        return render(request, "favs.html", context)