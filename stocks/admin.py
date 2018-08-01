from django.contrib import admin
from .models import Stock, Favorites


admin.site.register(Stock)
admin.site.register(Favorites)