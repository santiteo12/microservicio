# Microservicio de Documentos

Este proyecto es un microservicio Flask para la gestión de documentos, parte de un sistema de microservicios para la universidad.

## Requisitos Previos

- Python 3.8+
- Docker y Docker Compose (opcional, para ejecución con contenedores)
- k6 (para pruebas de carga)

## Instalación y Configuración

### Variables de Entorno

Crear un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
FLASK_CONTEXT=development
PORT=5002
MS_ALUMNO_URL=http://localhost:5001
MS_ACADEMICA_URL=http://localhost:5003
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
```

### Instalación Local

1. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

2. Ejecutar la aplicación:
```bash
python app.py
```

La aplicación estará disponible en `http://localhost:5002`

### Ejecución con Docker

1. Navegar al directorio docker:
```bash
cd docker
```

2. Ejecutar con Docker Compose:
```bash
docker-compose up --build
```

La aplicación estará disponible en `http://localhost:5002` o a través de Traefik en `https://documentos.universidad.localhost`

## Endpoints Disponibles

- `GET /health` - Verificar estado del servicio
- `GET /api/v1/certificado/{id}/pdf` - Generar certificado en PDF
- `GET /api/v1/certificado/{id}/odt` - Generar certificado en ODT
- `GET /api/v1/certificado/{id}/docx` - Generar certificado en DOCX
- `GET /api/v1/certificado/{id}/test` - Endpoint de prueba para k6

## Ejecutar Pruebas

### Pruebas Unitarias (Python)

Ejecutar todas las pruebas unitarias:
```bash
python -m unittest discover test/
```

Ejecutar pruebas específicas:
```bash
python test/test_app.py
python test/test_certificado.py
python test/test_endpoints.py
```

### Pruebas de Carga con k6

Asegurarse de que la aplicación esté ejecutándose.

Pruebas de carga normales:
```bash
k6 run test/test_k6.js
```

Pruebas de spike (alta carga):
```bash
k6 run test/spike_tests.js
```

### Configuración de Pruebas

Las pruebas unitarias usan el contexto de testing (`FLASK_CONTEXT=testing`).

Las pruebas de k6 requieren que la aplicación esté ejecutándose en `http://localhost:5002`.

## Arquitectura

- **Flask**: Framework web
- **Redis**: Cache y almacenamiento temporal
- **WeasyPrint**: Generación de PDFs
- **docxtpl**: Generación de documentos Word
- **Traefik**: Proxy reverso y load balancer
- **Docker**: Contenedorización

## Dependencias Externas

Este microservicio depende de otros microservicios:
- Microservicio de Alumnos (MS_ALUMNO_URL)
- Microservicio Académico (MS_ACADEMICA_URL)

Asegurarse de que estos servicios estén ejecutándose antes de iniciar este microservicio.
