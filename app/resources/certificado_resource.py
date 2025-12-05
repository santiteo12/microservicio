from flask import Blueprint, jsonify, send_file, abort
import logging

from app.services.alumno_service import AlumnoService

logger = logging.getLogger(__name__)
certificado_bp = Blueprint("certificado_bp", __name__)

@certificado_bp.route("/", methods=["GET"])
def index():
    return "OK"

@certificado_bp.route("/certificado/<int:alumno_id>/pdf", methods=["GET"])
def certificado_en_pdf(alumno_id: int):
    """
    Genera un PDF de certificado para el alumno.
    """
    try:
        pdf_io = AlumnoService.generar_certificado_alumno_regular(alumno_id, 'pdf')
    except Exception as e:
        logger.error(f"Error generando PDF: {str(e)}")
        return jsonify({"error": "Error generando documento PDF", "detalle": str(e)}), 500

    return send_file(
        pdf_io,
        mimetype="application/pdf",
        as_attachment=False,
        download_name=f"certificado_{alumno_id}.pdf"
    )
    

@certificado_bp.route("/certificado/<int:alumno_id>/docx", methods=["GET"])
def certificado_en_docx(alumno_id: int):

    try:
        docx_io = AlumnoService.generar_certificado_alumno_regular(alumno_id, 'docx')
    except Exception as e:
        logger.error(f"Error generando DOCX: {str(e)}")
        return jsonify({"error": "Error generando documento DOCX"}), 500

    return send_file(
        docx_io,
        mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        as_attachment=True,
        download_name=f"certificado_{alumno_id}.docx"
    )

@certificado_bp.route("/certificado/<int:alumno_id>/odt", methods=["GET"])
def certificado_en_odt(alumno_id: int):

    try:
        odt_io = AlumnoService.generar_certificado_alumno_regular(alumno_id, 'odt')
    except Exception as e:
        logger.error(f"Error generando ODT: {str(e)}")
        return jsonify({"error": "Error generando documento ODT"}), 500

    return send_file(
        odt_io,
        mimetype="application/vnd.oasis.opendocument.text",
        as_attachment=True,
        download_name=f"certificado_{alumno_id}.odt"
    )

@certificado_bp.route("/certificado/<int:alumno_id>/test", methods=["GET"])
def test_obtener_datos(alumno_id: int):
    alumno = AlumnoService.buscar_por_id(alumno_id)
    if not alumno:
        return jsonify({"error": "No se encontraron datos"}), 404

    context = AlumnoService._AlumnoService__obtener_alumno_compat(alumno)

    # Convertir objetos a diccionarios
    def to_dict(obj):
        if hasattr(obj, '__dict__'):
            result = {}
            for k, v in obj.__dict__.items():
                if not k.startswith('_'):
                    result[k] = to_dict(v) if hasattr(v, '__dict__') else v
            return result
        return obj

    serializable_context = {
        "alumno": to_dict(context["alumno"]),
        "especialidad": to_dict(context["especialidad"]),
        "facultad": to_dict(context["facultad"]),
        "universidad": to_dict(context["universidad"]),
        "fecha": context["fecha"],
        "url_base": context["url_base"]
    }

    return jsonify(serializable_context), 200
