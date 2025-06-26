from django.urls import path
from .views import (
    load_data,
    ventas_por_tienda,
    top_productos,
    reabastecimiento_por_proveedor,
    actualizar_tienda
)

urlpatterns = [
    path('load-data/', load_data),
    path('analytics/ventas-por-tienda/', ventas_por_tienda),
    path('analytics/top-productos/', top_productos),
    path('analytics/reabastecimiento-proveedor/', reabastecimiento_por_proveedor),
    path('dimension/tienda/<int:id>/', actualizar_tienda),
]

