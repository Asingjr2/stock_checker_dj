from django.urls import path

from .rest_views import CreateAPIView, DeleteAPIView


app_name="rest"
urlpatterns = [
    path('create/', CreateAPIView.as_view(), name="create"),
    path('delete/<uuid:pk>/', DeleteAPIView.as_view(), name="delete"),
]