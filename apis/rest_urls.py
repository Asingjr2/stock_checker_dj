from django.urls import path

from .rest_views import CreateAPIView, ListAPIView, DeleteAPIView


app_name="rest"
urlpatterns = [
    path('create/', CreateAPIView.as_view(), name="create"),
    path("list/", ListAPIView.as_view(), name="list"),
    path('delete/<uuid:pk>', DeleteAPIView.as_view(), name="delete"),
]