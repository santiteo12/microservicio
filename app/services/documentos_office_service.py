import os
import tempfile
from io import BytesIO
from abc import ABC, abstractmethod
import redis

from flask import current_app, render_template, url_for
from weasyprint import HTML
from docxtpl import DocxTemplate
import logging

logger = logging.getLogger(__name__)

# Redis client for caching
redis_client = redis.Redis(host=current_app.config.get('REDIS_HOST', 'localhost'), port=current_app.config.get('REDIS_PORT', 6379), db=0)

def url_fetcher(url):
    if url.scheme == 'file':
        path = url.path
        if path.startswith('/'):
            path = path[1:]  # Remove leading slash
        full_path = os.path.join(current_app.root_path, path)

        # Check if it's a PNG and if cached in Redis
        if full_path.endswith('.png'):
            cache_key = f"png:{full_path}"
            cached_data = redis_client.get(cache_key)
            if cached_data:
                logger.info(f"Loading PNG from Redis cache: {full_path}")
                return {'file_obj': BytesIO(cached_data), 'mime_type': 'image/png'}

            # Load from file and cache
            if os.path.exists(full_path):
                with open(full_path, 'rb') as f:
                    data = f.read()
                redis_client.set(cache_key, data, ex=3600)  # Cache for 1 hour
                logger.info(f"Cached PNG in Redis: {full_path}")
                return {'file_obj': BytesIO(data), 'mime_type': 'image/png'}

    # Fallback to default
    return HTML.default_url_fetcher(url)

class Document(ABC):
    @staticmethod
    @abstractmethod
    def generar(plantilla: str, context: dict, tipo: str) -> BytesIO:
        """
        - plantilla: nombre de la plantilla (sin extensión; busca en templates/certificado/)
        - context: dict con datos ya armados (nombre, apellido, especialidad, facultad, etc.)
        - tipo: tipo de documento ('pdf', 'docx', 'odt')
        - return: BytesIO con el contenido del documento
        """
        raise NotImplementedError

class PDFDocument(Document):
    @staticmethod
    def generar(plantilla: str, context: dict, tipo: str) -> BytesIO:
        try:
            # Renderiza template Jinja2 como HTML
            html_string = render_template(f"certificado/{plantilla}.html", **context)
            # base_url para que WeasyPrint resuelva static/ (imágenes, CSS)
            base_url = f"file://{current_app.root_path}/static/"
            bytes_pdf = HTML(string=html_string, base_url=base_url, url_fetcher=url_fetcher).write_pdf()
            pdf_io = BytesIO(bytes_pdf)
            pdf_io.seek(0)
            return pdf_io
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error generando PDF: {str(e)}")
            logger.error(f"Template: {plantilla}")
            logger.error(f"Context keys: {list(context.keys())}")
            raise e

class OfficeDocument(Document):
    @staticmethod
    def generar(plantilla: str, context: dict, tipo: str) -> BytesIO:
        path_template = os.path.join(
            current_app.root_path,
            "templates",
            "certificado",
            f"{plantilla}.odt"
        )
        doc = DocxTemplate(path_template)

        suffix = ".odt" if tipo == "odt" else ".docx"
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            temp_path = tmp.name

        try:
            doc.render(context)
            doc.save(temp_path)
            with open(temp_path, "rb") as f:
                buf = BytesIO(f.read())
                buf.seek(0)
        finally:
            try:
                os.remove(temp_path)
            except Exception:
                pass

        return buf

def obtener_tipo_documento(tipo: str):
    """Factory que devuelve la clase según tipo ('pdf', 'docx' o 'odt')."""
    tipos = {
        "pdf": PDFDocument,
        "docx": OfficeDocument,
        "odt": OfficeDocument,
    }
    return tipos.get(tipo)
