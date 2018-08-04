from rest_framework import serializers 

from stocks.models import Stock


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model= Stock
        fields = ["ticker_symbol", "pk", "user", "s_open", "s_close", "s_high", "s_low"]

    def get_url(self, obj):
        return obj.get_url()
