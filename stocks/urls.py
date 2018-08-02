from django.urls import path 

from . import views 
from .views import HomeView, StockDetailView, UserDetailView, StockListView, StockSearchView


app_name = "stocks"
urlpatterns = [
    path("home/", HomeView.as_view(), name="home"),
    path("stock_search/", StockSearchView.as_view(), name='stock_search'  ),
    path('<uuid:stock_id>/', StockDetailView.as_view(), name='stock_detail'),
    path('user/<str:username>/', UserDetailView.as_view(), name='user_detail'),
    path('stocks_list/', StockListView.as_view(), name='stocks_list'),
]
