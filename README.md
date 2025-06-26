# 📊 Sistema de Inventario - Data Warehouse

Un sistema completo de gestión de inventario construido con Django REST Framework y PostgreSQL, diseñado con arquitectura de Data Warehouse para análisis de datos empresariales.

## ✨ Características

- **🏗️ Arquitectura Data Warehouse**: Modelo dimensional con tablas de hechos y dimensiones
- **📈 Analytics en Tiempo Real**: Dashboards interactivos con métricas clave
- **🐳 Containerizado**: Implementación completa con Docker Compose
- **🔄 Datos Sintéticos**: Generación automática de datos realistas para testing
- **🌐 API RESTful**: Endpoints completos para integración y consultas
- **📱 Frontend Responsivo**: Dashboard web moderno y adaptable

## 🚀 Inicio Rápido

### Prerrequisitos
- Docker & Docker Compose
- Git

### Instalación

```bash
# Clonar el repositorio
git clone <tu-repositorio>
cd inventariobackend

# Levantar todos los servicios
docker-compose up --build

# ¡Listo! El sistema estará disponible en:
# - Frontend: http://localhost:8080
# - API: http://localhost:8000/api/
# - Admin Django: http://localhost:8000/admin/
```

El sistema se configura automáticamente con:
- ✅ Base de datos PostgreSQL
- ✅ Migraciones aplicadas
- ✅ 5,000+ registros de datos sintéticos
- ✅ Frontend servido por Nginx

## 🏛️ Arquitectura del Data Warehouse

### Modelo Dimensional

**Tablas de Dimensiones:**
- `DimFecha` - Dimensión temporal (año, mes, trimestre, día)
- `DimTienda` - Información de tiendas y ubicaciones
- `DimProducto` - Catálogo de productos con categorías
- `DimProveedor` - Datos de proveedores
- `DimCategoria` - Categorización de productos

**Tabla de Hechos:**
- `HechosInventario` - Métricas centrales (ventas, inventario, reabastecimiento)

### Diagrama de Relaciones
```
    DimFecha ──┐
    DimTienda ──┤
    DimProducto ──┼─── HechosInventario
    DimProveedor ──┤
    DimCategoria ──┘
```

## 🔌 API Endpoints

### Analytics
```http
GET /api/analytics/ventas-por-tienda/
GET /api/analytics/top-productos/
GET /api/analytics/reabastecimiento-proveedor/
```

### Gestión de Datos
```http
POST /api/load-data/
PUT /api/dimension/tienda/{id}/
```

### Ejemplos de Respuesta
```json
{
  "tienda": "Tienda Central",
  "total_vendido": 1250
}
```

## 🛠️ Tecnologías

**Backend:**
- Django 5.2.3
- Django REST Framework
- PostgreSQL 15
- Faker (generación de datos)

**Frontend:**
- HTML5 + CSS3 + Vanilla JavaScript
- Nginx (servidor web)

**DevOps:**
- Docker & Docker Compose
- Multi-stage builds
- Health checks automáticos

## 📊 Dashboard Features

- **Ventas por Tienda**: Ranking de rendimiento por ubicación
- **Top Productos**: Los 10 productos más vendidos
- **Reabastecimiento**: Análisis por proveedor
- **Responsive Design**: Optimizado para móviles y escritorio

## 🔧 Comandos Útiles

```bash
# Ver logs en tiempo real
docker-compose logs -f

# Acceder al shell de Django
docker-compose exec web python manage.py shell

# Generar más datos sintéticos
docker-compose exec web python manage.py populate_data

# Ejecutar migraciones manualmente
docker-compose exec web python manage.py migrate

# Crear superusuario
docker-compose exec web python manage.py createsuperuser
```

## 📁 Estructura del Proyecto

```
inventariobackend/
├── 🐳 docker-compose.yml
├── 📦 Dockerfile
├── 🌐 Dockerfile.frontend
├── ⚙️ requirements.txt
├── 🚀 entrypoint.sh
├── inventariobackend/          # Configuración Django
│   ├── settings.py
│   └── urls.py
├── api/                        # App principal
│   ├── models.py              # Modelos del Data Warehouse
│   ├── views.py               # Lógica de API
│   ├── serializers.py         # Serialización de datos
│   └── management/commands/
│       └── populate_data.py   # Generador de datos
└── frontend/
    └── index.html             # Dashboard interactivo
```

## 🎯 Casos de Uso

- **Retail Analytics**: Análisis de ventas y tendencias
- **Gestión de Inventario**: Control de stock y reabastecimiento
- **Business Intelligence**: Reportes ejecutivos y KPIs
- **Análisis Temporal**: Tendencias por períodos y estacionalidad

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Añadir nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 📞 Soporte

¿Tienes preguntas o encontraste un bug? 
- 🐛 [Reportar Issue](../../issues)
- 💬 [Discusiones](../../discussions)

---

⭐ **¿Te gustó el proyecto? ¡Dale una estrella!** ⭐
