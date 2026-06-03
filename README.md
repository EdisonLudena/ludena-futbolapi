# FutbolAPI - Sistema de Gestión de Jugadores y Rendimiento

Backend desarrollado en Python utilizando Django y Django REST Framework (DRF), asegurado mediante JSON Web Tokens (JWT). Permite la gestión de planteles, registro de encuentros deportivos y el seguimiento de métricas físicas y técnicas.

---

## 1. Instalación y Ejecución

### Prerrequisitos
* Python 3.10 o superior
* pip (gestor de paquetes)
* Entorno virtual (venv)

### Pasos para la configuración local

1. Acceder al directorio del proyecto:
    ```bash
    cd futbolapi-backend
    ```

2. Crear y activar el entorno virtual:
    * Windows:
        ```bash
        python -m venv venv
        venv\Scripts\activate
        ```
    * Linux/macOS:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3. Instalar las dependencias del sistema:
    ```bash
    pip install -r requirements.txt
    ```

4. Ejecutar las migraciones de la base de datos:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. Crear un usuario administrador (opcional):
    ```bash
    python manage.py createsuperuser
    ```

6. Iniciar el servidor de desarrollo:
    ```bash
    python manage.py runserver
    ```
    El servicio estará disponible en: `http://127.0.0.1:8000/`

7. Exposición pública con Ngrok (para pruebas externas):
    ```bash
    ngrok http 8000
    ```

---

## 2. Autenticación y Ejemplos de Uso

La API requiere autenticación mediante tokens JWT para proteger el acceso a los recursos de escritura y lectura avanzada.

### Obtención del Token (Login)
Enviar una petición HTTP `POST` con las credenciales de usuario.

* **URL:** `{{baseUrl}}/auth/login/`
* **Cuerpo (JSON):**

    ```json
    {
        "username": "admin",
        "password": "password_seguro"
    }
    ```

* **Respuesta (200 OK):** El servidor retornará un objeto con las llaves `access` y `refresh`. El string de `access` será utilizado como credencial.

### Consumo de Endpoints Protegidos
Para realizar solicitudes a rutas privadas, se debe incluir el token de acceso dentro de los encabezados HTTP utilizando el esquema Bearer.

* **Header Key:** `Authorization`
* **Header Value:** `Bearer <TU_TOKEN_ACCESS>`

**Ejemplo de creación de un recurso (POST):**
* **Endpoint:** `{{baseUrl}}/players/`
* **JSON Body:**

    ```json
    {
        "nombres": "Lionel",
        "apellidos": "Messi",
        "categoria": "Senior",
        "posicion": "Delantero",
        "is_active": true
    }
    ```

---

## 3. Listado de Endpoints

Todas las rutas del backend se estructuran bajo el prefijo general `/api/`.

### Módulo de Autenticación
* `POST /api/auth/register/` - Registro de nuevos usuarios y asignación de roles.
* `POST /api/auth/login/` - Autenticación de usuarios y entrega de tokens JWT.
* `POST /api/auth/token/refresh/` - Renovación de tokens de acceso expirados.
* `POST /api/auth/token/verify/` - Verificación del estado de validez de un token.
* `POST /api/auth/logout/` - Cierre de sesión e invalidación de tokens actuales.

### Módulo de Jugadores
* `GET /api/players/` - Listado general de jugadores registrados.
* `POST /api/players/` - Registro de un nuevo perfil de jugador.
* `GET /api/players/<pk>/` - Consulta detallada de la ficha de un jugador.
* `PUT /api/players/<pk>/` - Modificación completa de datos personales y deportivos.
* `DELETE /api/players/<pk>/` - Eliminación permanente del registro de un jugador.
* `GET /api/players/stats/` - Reporte estadístico global del rendimiento del plantel.

### Módulo de Partidos
* `GET /api/matches/` - Historial de partidos agendados y jugados.
* `POST /api/matches/` - Creación y programación de un nuevo partido.
* `GET /api/matches/<pk>/` - Información detallada de un encuentro específico.
* `PATCH /api/matches/<pk>/` - Cierre de partido y actualización del marcador definitivo.
* `GET /api/matches/stats/` - Métricas de rendimiento colectivo del equipo en el torneo.

### Rutas de Relación Anidadas
* `GET /api/players/<pk>/partidos/` - Historial exclusivo de partidos y métricas de desempeño de un jugador en particular.

---

## 4. Colección de Postman

El proyecto incluye un archivo de configuración listo para ser utilizado en clientes API.

### Instrucciones de uso:
1. Importar en Postman el archivo JSON adjunto en el repositorio: `futbolapi.postman_collection.json`.
2. Seleccionar o crear un entorno de variables en Postman (**Environment**).
3. Configurar la variable `{{baseUrl}}` con la dirección activa del servidor (ej. `http://127.0.0.1:8000/api` o la URL generada por Ngrok).
4. Ejecutar el endpoint de inicio de sesión. La colección contiene scripts de prueba automatizados que capturan y configuran la variable `{{token}}` automáticamente para el resto de peticiones de la sesión.
