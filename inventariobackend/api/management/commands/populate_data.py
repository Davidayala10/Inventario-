from django.core.management.base import BaseCommand
from django.db import transaction
from api.models import DimProducto, DimTienda, DimFecha, DimProveedor, DimCategoria, HechosInventario
from faker import Faker
import random
from datetime import datetime, timedelta
import sys

fake = Faker('es_ES')  # Usar español

class Command(BaseCommand):
    help = 'Pobla la base de datos con datos sintéticos realistas para inventario'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Limpiar datos existentes antes de poblar',
        )

    def handle(self, *args, **options):
        try:
            if options['clear']:
                self.stdout.write(self.style.WARNING('🗑️  Limpiando datos existentes...'))
                self.clear_data()

            self.stdout.write(self.style.SUCCESS('🚀 Iniciando población de datos...'))
            
            with transaction.atomic():
                # Crear datos de dimensiones
                categorias = self.create_categorias()
                self.stdout.write(f'✅ Creadas {len(categorias)} categorías')
                
                productos = self.create_productos(categorias)
                self.stdout.write(f'✅ Creados {len(productos)} productos')
                
                tiendas = self.create_tiendas()
                self.stdout.write(f'✅ Creadas {len(tiendas)} tiendas')
                
                proveedores = self.create_proveedores()
                self.stdout.write(f'✅ Creados {len(proveedores)} proveedores')
                
                fechas = self.create_fechas()
                self.stdout.write(f'✅ Creadas {len(fechas)} fechas')
                
                # Crear hechos de inventario
                hechos_count = self.create_hechos_inventario(productos, tiendas, fechas, proveedores)
                self.stdout.write(f'✅ Creados {hechos_count} registros de inventario')
                
            self.stdout.write(self.style.SUCCESS('🎉 ¡Datos sintéticos generados correctamente!'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error al generar datos: {str(e)}'))
            sys.exit(1)

    def clear_data(self):
        """Limpiar todos los datos existentes"""
        HechosInventario.objects.all().delete()
        DimProducto.objects.all().delete()
        DimCategoria.objects.all().delete()
        DimTienda.objects.all().delete()
        DimProveedor.objects.all().delete()
        DimFecha.objects.all().delete()

    def create_categorias(self):
        """Crear categorías realistas"""
        categorias_data = [
            {'nombre': 'Electrónicos', 'tipo': 'Tecnología', 'estacionalidad': 'Alta en navidad'},
            {'nombre': 'Ropa', 'tipo': 'Textil', 'estacionalidad': 'Estacional'},
            {'nombre': 'Hogar', 'tipo': 'Doméstico', 'estacionalidad': 'Baja'},
            {'nombre': 'Deportes', 'tipo': 'Recreativo', 'estacionalidad': 'Verano'},
            {'nombre': 'Libros', 'tipo': 'Educativo', 'estacionalidad': 'Inicio de año'},
            {'nombre': 'Alimentación', 'tipo': 'Consumible', 'estacionalidad': 'Constante'},
            {'nombre': 'Belleza', 'tipo': 'Personal', 'estacionalidad': 'Primavera'},
            {'nombre': 'Automóvil', 'tipo': 'Automotriz', 'estacionalidad': 'Baja'},
        ]
        
        categorias = []
        for data in categorias_data:
            categoria, created = DimCategoria.objects.get_or_create(
                nombre=data['nombre'],
                defaults=data
            )
            categorias.append(categoria)
        
        return categorias

    def create_productos(self, categorias):
        """Crear productos realistas por categoría"""
        productos = []
        productos_por_categoria = {
            'Electrónicos': ['Smartphone', 'Laptop', 'Tablet', 'Audífonos', 'Cámara', 'TV'],
            'Ropa': ['Camisa', 'Pantalón', 'Vestido', 'Zapatos', 'Chaqueta', 'Falda'],
            'Hogar': ['Mesa', 'Silla', 'Lámpara', 'Cojín', 'Cortinas', 'Alfombra'],
            'Deportes': ['Pelota', 'Raqueta', 'Pesas', 'Bicicleta', 'Casco', 'Uniforme'],
            'Libros': ['Novela', 'Manual', 'Diccionario', 'Revista', 'Comic', 'Enciclopedia'],
            'Alimentación': ['Arroz', 'Pasta', 'Aceite', 'Sal', 'Azúcar', 'Harina'],
            'Belleza': ['Shampoo', 'Crema', 'Perfume', 'Maquillaje', 'Jabón', 'Loción'],
            'Automóvil': ['Llanta', 'Aceite motor', 'Filtro', 'Batería', 'Frenos', 'Espejos'],
        }
        
        for categoria in categorias:
            productos_nombres = productos_por_categoria.get(categoria.nombre, ['Producto genérico'])
            for nombre_base in productos_nombres:
                for i in range(3):  # 3 variaciones por producto base
                    nombre_completo = f"{nombre_base} {fake.word().title()}"
                    precio = round(random.uniform(10.0, 2000.0), 2)
                    unidad = random.choice(['unidad', 'kg', 'litro', 'metro', 'caja', 'paquete'])
                    
                    producto = DimProducto.objects.create(
                        nombre=nombre_completo,
                        categoria=categoria,
                        unidad_medida=unidad,
                        precio=precio
                    )
                    productos.append(producto)
        
        return productos

    def create_tiendas(self):
        """Crear tiendas realistas"""
        ciudades_mexico = ['Ciudad de México', 'Guadalajara', 'Monterrey', 'Puebla', 'Tijuana', 'León', 'Juárez', 'Torreón', 'Querétaro', 'San Luis Potosí']
        tipos_tienda = ['Departamental', 'Especializada', 'Supermercado', 'Boutique', 'Centro comercial']
        
        tiendas = []
        for i in range(15):
            ciudad = random.choice(ciudades_mexico)
            tienda = DimTienda.objects.create(
                nombre=f"Tienda {fake.company()}",
                ciudad=ciudad,
                estado=self.get_estado_por_ciudad(ciudad),
                tipo_tienda=random.choice(tipos_tienda),
                direccion=fake.address()
            )
            tiendas.append(tienda)
        
        return tiendas

    def get_estado_por_ciudad(self, ciudad):
        """Mapear ciudades a estados"""
        mapeo = {
            'Ciudad de México': 'CDMX',
            'Guadalajara': 'Jalisco',
            'Monterrey': 'Nuevo León',
            'Puebla': 'Puebla',
            'Tijuana': 'Baja California',
            'León': 'Guanajuato',
            'Juárez': 'Chihuahua',
            'Torreón': 'Coahuila',
            'Querétaro': 'Querétaro',
            'San Luis Potosí': 'San Luis Potosí'
        }
        return mapeo.get(ciudad, 'Estado')

    def create_proveedores(self):
        """Crear proveedores realistas"""
        paises = ['México', 'Estados Unidos', 'China', 'Alemania', 'Brasil', 'Japón']
        tipos = ['Fabricante', 'Distribuidor', 'Mayorista', 'Importador']
        
        proveedores = []
        for i in range(12):
            proveedor = DimProveedor.objects.create(
                nombre=fake.company(),
                pais=random.choice(paises),
                tipo=random.choice(tipos)
            )
            proveedores.append(proveedor)
        
        return proveedores

    def create_fechas(self):
        """Crear fechas para el último año"""
        fechas = []
        fecha_inicio = datetime.now() - timedelta(days=365)
        
        for i in range(365):
            fecha = fecha_inicio + timedelta(days=i)
            trimestre = (fecha.month - 1) // 3 + 1
            
            fecha_obj, created = DimFecha.objects.get_or_create(
                fecha=fecha.date(),
                defaults={
                    'anio': fecha.year,
                    'mes': fecha.month,
                    'dia': fecha.day,
                    'trimestre': trimestre
                }
            )
            fechas.append(fecha_obj)
        
        return fechas

    def create_hechos_inventario(self, productos, tiendas, fechas, proveedores):
        """Crear registros de hechos de inventario"""
        hechos = []
        batch_size = 1000
        
        # Generar datos más realistas
        for i in range(8000):  # Aumentar cantidad para mejor análisis
            # Simular patrones realistas
            cantidad_base = random.randint(50, 500)
            variacion_venta = random.uniform(0.1, 0.4)  # 10-40% de ventas
            variacion_reabastecimiento = random.uniform(0.05, 0.3)  # 5-30% de reabastecimiento
            
            cantidad_vendida = int(cantidad_base * variacion_venta)
            cantidad_reabastecida = int(cantidad_base * variacion_reabastecimiento)
            cantidad_disponible = cantidad_base + cantidad_reabastecida - cantidad_vendida
            
            # Asegurar que la cantidad disponible no sea negativa
            cantidad_disponible = max(cantidad_disponible, 0)
            
            hecho = HechosInventario(
                producto=random.choice(productos),
                tienda=random.choice(tiendas),
                fecha=random.choice(fechas),
                proveedor=random.choice(proveedores),
                cantidad_disponible=cantidad_disponible,
                cantidad_vendida=cantidad_vendida,
                cantidad_reabastecida=cantidad_reabastecida
            )
            hechos.append(hecho)
            
            # Insertar en lotes para mejor rendimiento
            if len(hechos) >= batch_size:
                HechosInventario.objects.bulk_create(hechos)
                hechos = []
                self.stdout.write(f'📊 Procesados {i + 1} registros...')
        
        # Insertar los registros restantes
        if hechos:
            HechosInventario.objects.bulk_create(hechos)
        
        return HechosInventario.objects.count()