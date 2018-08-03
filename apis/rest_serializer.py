from rest_framework import serializers 

from stocks.models import Stock


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model= Stock
        fields = ["ticker_symbol", "pk", "user"]

    def get_url(self, obj):
        return obj.get_url()
