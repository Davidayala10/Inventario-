from rest_framework import serializers
from .models import HechosInventario, DimTienda

class HechosInventarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = HechosInventario
        fields = '__all__'

class DimTiendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DimTienda
        fields = '__all__'
