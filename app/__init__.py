import os
from flask import Flask
from flask_marshmallow import Marshmallow

# Solo necesitamos Marshmallow para esquemas (validación/serialización de respuestas)
ma = Marshmallow()

def create_app():
    """Factory para crear instancias de la app Flask."""
    app = Flask(__name__, instance_relative_config=False)

    # Configuración básica
    app.config["FLASK_CONTEXT"] = os.getenv("FLASK_CONTEXT", "development")

    # Cargar variables de entorno para las URLs de otros microservicios
    app.config["MS_ALUMNO_URL"] = os.getenv("MS_ALUMNO_URL", "http://localhost:5001")
    app.config["MS_ACADEMICA_URL"] = os.getenv("MS_ACADEMICA_URL", "http://localhost:5003")

    # Inicializar extensiones
    ma.init_app(app)

    # Registrar blueprints
    from app.resources.certificado_resource import certificado_bp
    app.register_blueprint(certificado_bp, url_prefix="/api/v1")

    @app.route("/health")
    def health():
        return {"status": "ok", "service": "ms-documentos"}, 200

    return app
