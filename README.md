# FlexiAhorro

## Descripción
FlexiAhorro es una aplicación desarrollada como parte del **Reto del Ahorro en Laboratoria Innova BCP**. Permite a los usuarios establecer y gestionar metas de ahorro, visualizar reportes de ingresos y egresos, y realizar un seguimiento de su progreso ahorro a través de una API REST.

## Características principales
- Creación y gestión de metas de ahorro.
- Seguimiento de ingresos, egresos y ganancias diarias.
- Reportes movimiento de ahorro detallados.
- Autenticación y gestión de usuarios.

## Documentación de la API
La API sigue el estándar **OAS 3.0** y su documentación está disponible en:
```
/api/schema/swagger-ui/
```

### Endpoints disponibles

#### **Niveles**
- `GET /api/v1/levels/` → Obtener información sobre los niveles de ahorro.

#### **Transacciones**
- `GET /api/v1/transactions/daily-profit/` → Obtener la ganancia diaria.
- `GET /api/v1/transactions/report/` → Obtener reportes de ingresos, egresos y ganancias.

#### **Ahorros**
- `GET /api/v1/savings-goals/` → Listar metas de ahorro.
- `POST /api/v1/savings-goals/` → Crear una nueva meta de ahorro.
- `GET /api/v1/savings-goals/{id}/` → Obtener detalles de una meta de ahorro específica.
- `PUT /api/v1/savings-goals/{id}/` → Actualizar una meta de ahorro.
- `PATCH /api/v1/savings-goals/{id}/` → Modificar parcialmente una meta de ahorro.
- `DELETE /api/v1/savings-goals/{id}/` → Eliminar una meta de ahorro.

#### **Usuarios**
- `GET /api/v1/users/` → Listar usuarios.
- `POST /api/v1/users/` → Crear un nuevo usuario.
- `GET /api/v1/users/{id}/` → Obtener información de un usuario específico.
- `PUT /api/v1/users/{id}/` → Actualizar un usuario.
- `PATCH /api/v1/users/{id}/` → Modificar parcialmente un usuario.
- `DELETE /api/v1/users/{id}/` → Eliminar un usuario.

## Instalación y configuración
### **Requisitos**
- Python 4.0+
- Django y Django REST Framework
- Docker (opcional para despliegue en contenedores)

### **Instalación**
1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu_usuario/flexiahorro.git
   cd flexiahorro
   ```
2. Crea y activa un entorno virtual:
   ```bash
   python -m venv env
   source env/bin/activate  # En Windows usa 'env\Scripts\activate'
   ```
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Aplica migraciones:
   ```bash
   python manage.py migrate
   ```
5. Ejecuta el servidor:
   ```bash
   python manage.py runserver
   ```

## Despliegue con Docker
Si deseas desplegar la aplicación en un contenedor Docker:
```bash
docker-compose up --build
```

## Diseño de la interfaz
El diseño de la aplicación está basado en Figma y cuenta con las siguientes pantallas:
- **Selección de tipo de ahorro**: Opción para ahorrar por porcentaje o mediante un club de ahorro.
- **Niveles de ahorro**: Progresión por niveles.
- **Creación de meta de ahorro**: Configuración de una meta personalizada.
- **Selección de porcentaje de ahorro**: Configuración del porcentaje de ahorro automático.
- **Resumen de ahorros diarios**: Visualización de la ganancia y progreso.
- **Dashboard financiero**: Reportes gráficos de ingresos y egresos.

## Autenticación
La API utiliza autenticación basada en tokens. Para acceder a los endpoints protegidos, es necesario incluir un token en los headers de las peticiones:
```bash
Authorization: Token <tu_token>
```

## Contribuciones
Si deseas contribuir al proyecto, por favor:
1. Crea un **fork** del repositorio.
2. Crea una nueva rama con tu funcionalidad.
3. Realiza un **pull request** para revisión.

## Contacto
Para más información, puedes contactarnos en: **soporte@flexiahorro.com**

---
**Versión:** 1.0.0


