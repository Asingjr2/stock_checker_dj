from django.urls import path

from stocks.rest_views import CreateApiView, UpdateDeleteApiView, ListApiView, RetrieveApiView

app_name="rest"
urlpatterns = [
    path('create/', CreateApiView.as_view(), name="create"),
    path('list/', ListApiView.as_view(), name="list"),
    path('update_delete/<uuid:pk>/', UpdateDeleteApiView.as_view(), name="update-delete"),
    path('specific_blog/<uuid:pk>/', RetrieveApiView.as_view(), name="retrieve"),
]