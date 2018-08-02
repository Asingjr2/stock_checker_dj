import time
from django.views import View
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date, datetime, timedelta
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404

import requests

from .models import Stock, Favorites


# Create your views here.
class HomeView(View):

    def get(self, request):
        queryset = Favorites.objects.all().filter(user__id = (self.request.user.id))
        return render(request, "stocks/home.html", {"favorites": queryset})

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["favorites"] = Favorites.objects.all().filter(user__id = (self.request.user.id))
    #     print(Favorites.objects.all().count())
    #     return context


class StockSearchView(View):
    def get(self, request):
        if "current_ticker" in request.session:
            print("there is a stock")
            # Fri1 = timedelta(days=-1)   # Will subtract day if calendar day falls on Sat
            # Fri2 = timedelta(days=-2)   # Will subtract day if calendar day falls on Sun
            # today= datetime.today()
            
            # if today.strftime("%A") == "Saturday":
            #     today += Fri1
            # if today.strftime("%A") == "Sunday":
            #     today += Fri2

            # today_formatted = today.strftime("%Y-%m-%d")

            # response = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + str(request.session["current_ticker"]) + "&apikey=HVS4381TKE7Y9YOS")
            # ss = response.json()['Time Series (Daily)'][today_formatted]
            # stock_data = [ ss["1. open"], ss["2. high"], ss["3. low"], ss["4. close"]  ]
            # context = {
            #     # "stock_data": stock_data,
            #     "stock": request.session["current_ticker"]
            # }
            # return render(request, "stocks/stock_search.html", context)
            return render(request, "stocks/stock_search.html")

        # if "current_ticker" not in request.session:
        #     return redirect("/stocks/home/")


    def post(self, request):
        new_stock = str(request.POST["ticker"]).upper()
        request.session["current_stock"] = new_stock
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