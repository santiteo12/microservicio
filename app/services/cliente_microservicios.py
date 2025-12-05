import requests
from flask import current_app
from typing import Optional, Dict, Any
import logging
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

logger = logging.getLogger(__name__)

class ClienteMicroservicios:
    """
    Cliente centralizado para comunicarse con otros microservicios.
    Implementa reintentos y manejo de errores.
    """

    @staticmethod
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type(requests.RequestException),
        before_sleep=lambda retry_state: logger.warning(f"Reintentando obtener_alumno para {retry_state.args[0]}: intento {retry_state.attempt_number}")
    )
    def obtener_alumno(alumno_id: int) -> Optional[Dict[str, Any]]:
        """
        Llama a ms-alumno para obtener datos del alumno.

        Respuesta esperada del ms-alumno:
        {
            "id": 1,
            "nombre": "Juan",
            "apellido": "Pérez",
            "nro_legajo": "12345",
            "nrodocumento": "35123456"
        }
        """
        try:
            url = f"{current_app.config['MS_ALUMNO_URL']}/api/v1/alumno/{alumno_id}"
            response = requests.get(url, timeout=5)

            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"ms-alumno retornó {response.status_code} para alumno {alumno_id}")
                return None
        except requests.RequestException as e:
            logger.error(f"Error conectando a ms-alumno: {str(e)}")
            return None

    @staticmethod
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type(requests.RequestException),
        before_sleep=lambda retry_state: logger.warning(f"Reintentando obtener_datos_academicos para {retry_state.args[0]}: intento {retry_state.attempt_number}")
    )
    def obtener_datos_academicos(alumno_id: int) -> Optional[Dict[str, Any]]:
        """
        Llama a ms-gestion-academica para obtener especialidad, facultad, etc.

        Respuesta esperada:
        {
            "especialidad": "Ingeniería en Sistemas",
            "facultad": "Facultad de Ingeniería",
            "plan": "Plan 2020",
            "año_inscripcion": 2020
        }
        """
        try:
            url = f"{current_app.config['MS_ACADEMICA_URL']}/api/v1/academico/{alumno_id}"
            response = requests.get(url, timeout=5)

            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"ms-academica retornó {response.status_code} para alumno {alumno_id}")
                return None
        except requests.RequestException as e:
            logger.error(f"Error conectando a ms-academica: {str(e)}")
            return None

    @staticmethod
    def obtener_datos_completos(alumno_id: int) -> Optional[Dict[str, Any]]:
        """
        Orquesta: obtiene datos de alumno + datos académicos y los combina.
        Devuelve None si falla algo crítico.
        """
        datos_alumno = ClienteMicroservicios.obtener_alumno(alumno_id)
        if not datos_alumno:
            return None
        
        datos_academicos = ClienteMicroservicios.obtener_datos_academicos(alumno_id)
        if not datos_academicos:
            # Podría devolver solo datos del alumno o fallar. Depende de tu requerimiento.
            logger.warning(f"No se obtuvieron datos académicos para alumno {alumno_id}")
            datos_academicos = {}
        
        # Combinar ambos en un único contexto para el certificado
        contexto = {
            **datos_alumno,
            **datos_academicos
        }
        return contexto