"""
Mock services para pruebas locales del microservicio de gestión de documentos.
Simula ms-alumnos en puerto 5001 y ms-academica en puerto 5003.

Uso:
    python mock_services.py
"""

from flask import Flask, jsonify, request
import sys
from datetime import datetime, timedelta
import random

app = Flask(__name__)

# Base de datos simulada
ALUMNOS_DB = {
    "1": {
        "id": "1",
        "nombre": "Juan",
        "apellido": "Pérez García",
        "nro_legajo": "2024001",
        "nrodocumento": "35123456",
        "tipo_documento": "DNI",
        "sexo": "M",
        "fecha_nacimiento": "1995-05-15",
        "fecha_ingreso": "2020-03-01",
        "email": "juan.perez@estudiantes.utn.edu.ar"
    },
    "2": {
        "id": "2",
        "nombre": "María",
        "apellido": "González López",
        "nro_legajo": "2024002",
        "nrodocumento": "36234567",
        "tipo_documento": "DNI",
        "sexo": "F",
        "fecha_nacimiento": "1996-08-22",
        "fecha_ingreso": "2020-03-01",
        "email": "maria.gonzalez@estudiantes.utn.edu.ar"
    },
    "3": {
        "id": "3",
        "nombre": "Carlos",
        "apellido": "Martínez Ruiz",
        "nro_legajo": "2024003",
        "nrodocumento": "37345678",
        "tipo_documento": "DNI",
        "sexo": "M",
        "fecha_nacimiento": "1997-12-10",
        "fecha_ingreso": "2021-03-01",
        "email": "carlos.martinez@estudiantes.utn.edu.ar"
    }
}

ACADEMICA_DB = {
    "1": {
        "alumno_id": "1",
        "carrera": "Ingeniería en Sistemas de Información",
        "especialidad": "Sistemas",
        "facultad": {
            "nombre": "Facultad de Ingeniería",
            "ciudad": "Mendoza",
            "provincia": "Mendoza"
        },
        "universidad": {
            "nombre": "Universidad Tecnológica Nacional",
            "sigla": "UTN"
        },
        "plan_estudio": "2020",
        "estado": "Activo",
        "promedio": 7.85,
        "materias_aprobadas": 24,
        "materias_totales": 30
    },
    "2": {
        "alumno_id": "2",
        "carrera": "Ingeniería en Sistemas de Información",
        "especialidad": "Sistemas",
        "facultad": {
            "nombre": "Facultad de Ingeniería",
            "ciudad": "Mendoza",
            "provincia": "Mendoza"
        },
        "universidad": {
            "nombre": "Universidad Tecnológica Nacional",
            "sigla": "UTN"
        },
        "plan_estudio": "2020",
        "estado": "Activo",
        "promedio": 8.25,
        "materias_aprobadas": 26,
        "materias_totales": 30
    },
    "3": {
        "alumno_id": "3",
        "carrera": "Ingeniería Civil",
        "especialidad": "Estructuras",
        "facultad": {
            "nombre": "Facultad de Ingeniería",
            "ciudad": "Mendoza",
            "provincia": "Mendoza"
        },
        "universidad": {
            "nombre": "Universidad Tecnológica Nacional",
            "sigla": "UTN"
        },
        "plan_estudio": "2020",
        "estado": "Activo",
        "promedio": 7.50,
        "materias_aprobadas": 22,
        "materias_totales": 30
    }
}

# ========== ENDPOINTS MS-ALUMNOS ==========

@app.route('/api/v1/alumno/<alumno_id>', methods=['GET'])
def get_alumno(alumno_id):
    """Obtiene datos de un alumno específico."""
    if alumno_id in ALUMNOS_DB:
        return jsonify(ALUMNOS_DB[alumno_id]), 200
    else:
        return jsonify({
            "error": f"Alumno con ID {alumno_id} no encontrado",
            "code": "ALUMNO_NOT_FOUND"
        }), 404

@app.route('/api/v1/alumnos', methods=['GET'])
def get_alumnos():
    """Obtiene lista de todos los alumnos."""
    return jsonify({
        "total": len(ALUMNOS_DB),
        "alumnos": list(ALUMNOS_DB.values())
    }), 200

@app.route('/health', methods=['GET'])
def health_alumnos():
    """Health check para ms-alumnos."""
    return jsonify({
        "status": "healthy",
        "service": "ms-alumnos",
        "timestamp": datetime.utcnow().isoformat()
    }), 200

# ========== ENDPOINTS MS-ACADEMICA ==========

@app.route('/api/v1/academico/<alumno_id>', methods=['GET'])
def get_academico(alumno_id):
    """Obtiene datos académicos de un alumno específico."""
    if alumno_id in ACADEMICA_DB:
        return jsonify(ACADEMICA_DB[alumno_id]), 200
    else:
        return jsonify({
            "error": f"Datos académicos para alumno {alumno_id} no encontrados",
            "code": "ACADEMICO_NOT_FOUND"
        }), 404

@app.route('/api/v1/academicos', methods=['GET'])
def get_academicos():
    """Obtiene lista de todos los registros académicos."""
    return jsonify({
        "total": len(ACADEMICA_DB),
        "academicos": list(ACADEMICA_DB.values())
    }), 200

@app.route('/health', methods=['GET'])
def health_academica():
    """Health check para ms-academica."""
    return jsonify({
        "status": "healthy",
        "service": "ms-academica",
        "timestamp": datetime.utcnow().isoformat()
    }), 200

# ========== ENDPOINT DE DIAGNÓSTICO ==========

@app.route('/mock/info', methods=['GET'])
def mock_info():
    """Información sobre los mocks disponibles."""
    return jsonify({
        "service": "Mock Microservices",
        "endpoints": {
            "alumnos": [
                "GET /api/v1/alumno/<id>",
                "GET /api/v1/alumnos",
                "GET /health"
            ],
            "academica": [
                "GET /api/v1/academico/<id>",
                "GET /api/v1/academicos",
                "GET /health"
            ]
        },
        "available_ids": list(ALUMNOS_DB.keys()),
        "timestamp": datetime.utcnow().isoformat()
    }), 200

if __name__ == '__main__':
    # Imprimir información de inicio
    print("=" * 60)
    print("MOCK MICROSERVICES - Gestión de Documentos")
    print("=" * 60)
    print("\nServicios disponibles:")
    print("  - MS-ALUMNOS en http://localhost:5001")
    print("  - MS-ACADEMICA en http://localhost:5003")
    print("\nEndpoints:")
    print("  GET /api/v1/alumno/<id>       - Datos de alumno")
    print("  GET /api/v1/alumnos           - Lista de alumnos")
    print("  GET /api/v1/academico/<id>    - Datos académicos")
    print("  GET /api/v1/academicos        - Lista académica")
    print("  GET /health                   - Health check")
    print("  GET /mock/info                - Info de mocks")
    print("\nIDs disponibles:", ", ".join(ALUMNOS_DB.keys()))
    print("\nNota: para pruebas, configura:")
    print("  MS_ALUMNO_URL=http://localhost:5001")
    print("  MS_ACADEMICA_URL=http://localhost:5003")
    print("\n" + "=" * 60)
    
    # Levantar en ambos puertos (simulando dos servicios)
    print("\nIniciando mock en puerto 5001...")
    app.run(host='0.0.0.0', port=5001, debug=False)
