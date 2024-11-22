from rest_framework import serializers
from .models import Company, StockData

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'sector_level1', 'sector_level2']

class StockDataSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    class Meta:
        model = StockData
        fields = ['id', 'company', 'asof', 'volume', 'close_usd']
