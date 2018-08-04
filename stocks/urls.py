from django.urls import path 

from . import views 
from .views import HomeView, StockSearchView, RefreshAllStocks


app_name = "stocks"
urlpatterns = [
    path("home/", HomeView.as_view(), name="home"),
    path("stock_search/", StockSearchView.as_view(), name='stock_search'),
    path("refresh_all/", RefreshAllStocks.as_view(), name="refresh_all")
]
