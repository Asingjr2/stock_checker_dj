from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput, HiddenInput

from .models import Stock

class StockCreateForm(ModelForm):
    class Meta:
        model = Stock
        fields = ["ticker_symbol"]
        class Meta:
            labels = {
                    "ticker":"fun"
        }
        widgets = {
            "ticker_symbol": forms.TextInput( attrs = {
                "class" : "form-control mr-sm-2",
                "placeholder" : "enter ticker...", 
                "aria-label": "Search", 
                "name":"ticker", 
                "type":"seach", 
            })
        
        }
