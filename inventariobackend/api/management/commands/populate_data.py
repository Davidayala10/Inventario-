from django.core.management.base import BaseCommand
from api.models import DimProducto, DimTienda, DimFecha, DimProveedor, DimCategoria, HechosInventario
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

class Command(BaseCommand):
    help = 'Pobla la base de datos con datos sintéticos realistas'

    def handle(self, *args, **kwargs):
        # Crear categorías
        categorias = [DimCategoria.objects.create(nombre=fake.word()) for _ in range(5)]

        # Crear productos
        productos = []
        for _ in range(100):
            producto = DimProducto.objects.create(
                nombre=fake.word(),
                categoria=random.choice(categorias),
                unidad_medida=random.choice(['unidad', 'litro', 'kg']),
                precio=round(random.uniform(5.0, 500.0), 2)
            )
            productos.append(producto)

        # Crear tiendas
        tiendas = [DimTienda.objects.create(nombre=fake.company(), direccion=fake.address()) for _ in range(10)]

        # Crear proveedores
        proveedores = [DimProveedor.objects.create(nombre=fake.company()) for _ in range(10)]

        # Crear fechas
        fechas = []
        for i in range(365):
            fecha = datetime.today() - timedelta(days=i)
            trimestre = (fecha.month - 1) // 3 + 1  # Cálculo del trimestre (1-4)
            fechas.append(DimFecha.objects.create(
                fecha=fecha,
                anio=fecha.year,
                mes=fecha.month,
                dia=fecha.day,
                trimestre=trimestre
            ))

        # Crear registros de hechos
        for _ in range(5000):
            HechosInventario.objects.create(
                producto=random.choice(productos),
                tienda=random.choice(tiendas),
                fecha=random.choice(fechas),
                proveedor=random.choice(proveedores),
                cantidad_disponible=random.randint(10, 100),
                cantidad_vendida=random.randint(0, 50),
                cantidad_reabastecida=random.randint(0, 50)
            )

        self.stdout.write(self.style.SUCCESS('¡Datos sintéticos generados correctamente!'))
