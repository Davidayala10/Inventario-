from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import HechosInventario
from .serializers import HechosInventarioSerializer
from .models import DimTienda
from .serializers import DimTiendaSerializer



@api_view(['POST'])
def load_data(request):
    serializer = HechosInventarioSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.db.models import Sum

@api_view(['GET'])
def ventas_por_tienda(request):
    datos = (
        HechosInventario.objects
        .values('tienda__nombre')
        .annotate(total_vendido=Sum('cantidad_vendida'))
        .order_by('-total_vendido')
    )
    resultados = [
        {"tienda": d['tienda__nombre'], "total_vendido": d['total_vendido']}
        for d in datos
    ]
    return Response(resultados)


@api_view(['GET'])
def top_productos(request):
    datos = (
        HechosInventario.objects
        .values('producto__nombre')
        .annotate(total_vendido=Sum('cantidad_vendida'))
        .order_by('-total_vendido')[:10]  # Top 10 productos
    )
    resultados = [
        {"producto": d['producto__nombre'], "total_vendido": d['total_vendido']}
        for d in datos
    ]
    return Response(resultados)


@api_view(['GET'])
def reabastecimiento_por_proveedor(request):
    datos = (
        HechosInventario.objects
        .values('proveedor__nombre')
        .annotate(total_reabastecido=Sum('cantidad_reabastecida'))
        .order_by('-total_reabastecido')
    )
    resultados = [
        {"proveedor": d['proveedor__nombre'], "total_reabastecido": d['total_reabastecido']}
        for d in datos
    ]
    return Response(resultados)



@api_view(['PUT'])
def actualizar_tienda(request, id):
    try:
        tienda = DimTienda.objects.get(id=id)
    except DimTienda.DoesNotExist:
        return Response({"error": "Tienda no encontrada"}, status=404)

    serializer = DimTiendaSerializer(tienda, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


