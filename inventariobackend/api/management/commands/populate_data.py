from django.core.management.base import BaseCommand
from api.models import DimFecha, DimTienda, DimProveedor, DimCategoria, DimProducto, HechosInventario
from faker import Faker

class Command(BaseCommand):
    help = 'Poblar la base de datos con datos de prueba'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Poblar DimFecha con datos ficticios
        fechas = []
        for _ in range(10):  # Cambia 10 por la cantidad que desees
            fecha = fake.date_this_decade()
            mes = fecha.month
            trimestre = (mes - 1) // 3 + 1  # Calculando el trimestre
            anio = fecha.year
            fechas.append(DimFecha.objects.create(fecha=fecha, mes=mes, trimestre=trimestre, anio=anio))
        
        # Poblar DimTienda con datos ficticios
        tiendas = []
        for _ in range(5):
            tienda = DimTienda.objects.create(
                nombre=fake.company(),
                ciudad=fake.city(),
                estado=fake.state(),
                tipo_tienda=fake.word()
            )
            tiendas.append(tienda)
        
        # Poblar DimProveedor con datos ficticios
        proveedores = []
        for _ in range(5):
            proveedor = DimProveedor.objects.create(
                nombre=fake.company(),
                pais=fake.country(),
                tipo=fake.word()
            )
            proveedores.append(proveedor)
        
        # Poblar DimCategoria con datos ficticios
        categorias = []
        for _ in range(5):
            categoria = DimCategoria.objects.create(
                nombre=fake.word(),
                tipo=fake.word(),
                estacionalidad=fake.word()
            )
            categorias.append(categoria)
        
        # Poblar DimProducto con datos ficticios
        productos = []
        for _ in range(10):
            producto = DimProducto.objects.create(
                nombre=fake.word(),
                categoria=fake.random_element(categorias),  # Elegir una categoría aleatoria
                unidad_medida=fake.word(),
                precio=fake.random_number(digits=5)  # Precio aleatorio entre 10000 y 99999
            )
            productos.append(producto)
        
        # Poblar HechosInventario con datos ficticios
        for _ in range(100):  # Cambia 100 por la cantidad que desees
            HechosInventario.objects.create(
                tienda=fake.random_element(tiendas),
                producto=fake.random_element(productos),
                fecha=fake.random_element(fechas),
                proveedor=fake.random_element(proveedores),
                cantidad_disponible=fake.random_number(digits=3),  # Cantidad disponible entre 0 y 999
                cantidad_vendida=fake.random_number(digits=3),
                cantidad_reabastecida=fake.random_number(digits=3)
            )

        self.stdout.write(self.style.SUCCESS('Base de datos poblada con éxito!'))
