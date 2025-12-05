from app.models.alumno import Alumno

class AlumnoRepository:
    _alumnos = []
    _next_id = 1

    @staticmethod
    def crear(alumno: Alumno) -> Alumno:
        AlumnoRepository._init_data()
        alumno.id = AlumnoRepository._next_id
        AlumnoRepository._next_id += 1
        AlumnoRepository._alumnos.append(alumno)
        return alumno

    @staticmethod
    def buscar_por_id(id: int) -> Alumno:
        AlumnoRepository._init_data()
        for alumno in AlumnoRepository._alumnos:
            if alumno.id == id:
                return alumno
        return None

    @staticmethod
    def buscar_todos() -> list[Alumno]:
        AlumnoRepository._init_data()
        return AlumnoRepository._alumnos.copy()

    @staticmethod
    def actualizar(id: int, alumno: Alumno) -> Alumno:
        AlumnoRepository._init_data()
        for i, a in enumerate(AlumnoRepository._alumnos):
            if a.id == id:
                alumno.id = id
                AlumnoRepository._alumnos[i] = alumno
                return alumno
        return None

    @staticmethod
    def borrar_por_id(id: int) -> bool:
        AlumnoRepository._init_data()
        for i, alumno in enumerate(AlumnoRepository._alumnos):
            if alumno.id == id:
                del AlumnoRepository._alumnos[i]
                return True
        return False

    @staticmethod
    def _init_data():
        """Inicializa datos de prueba si no existen."""
        if AlumnoRepository._alumnos:
            return

        from app.models.tipodocumento import TipoDocumento
        from app.models.especialidad import Especialidad

        # Crear tipos de documento de prueba
        dni = TipoDocumento()
        dni.id = 1
        dni.sigla = "DNI"
        dni.nombre = "Documento Nacional de Identidad"

        # Crear mocks para facultad y universidad
        class MockUniversidad:
            def __init__(self, nombre):
                self.nombre = nombre

        class MockFacultad:
            def __init__(self, nombre, ciudad, universidad):
                self.nombre = nombre
                self.ciudad = ciudad
                self.universidad = universidad

        utn = MockUniversidad("Universidad Tecnológica Nacional")
        facultad_ing = MockFacultad("Facultad de Ingeniería", "Mendoza", utn)

        # Crear especialidades de prueba
        especialidad1 = Especialidad()
        especialidad1.id = 1
        especialidad1.nombre = "Ingeniería en Sistemas de Información"
        especialidad1.letra = "ISI"
        especialidad1.observacion = None
        especialidad1.facultad = facultad_ing
        especialidad1.universidad = utn

        especialidad2 = Especialidad()
        especialidad2.id = 2
        especialidad2.nombre = "Ingeniería Civil"
        especialidad2.letra = "IC"
        especialidad2.observacion = None
        especialidad2.facultad = facultad_ing
        especialidad2.universidad = utn

        # Crear alumnos de prueba
        alumno1 = Alumno()
        alumno1.id = 1
        alumno1.nombre = "Juan"
        alumno1.apellido = "Pérez García"
        alumno1.nrodocumento = "35123456"
        alumno1.tipo_documento = dni
        alumno1.nro_legajo = 2024001
        alumno1.especialidad = especialidad1

        alumno2 = Alumno()
        alumno2.id = 2
        alumno2.nombre = "María"
        alumno2.apellido = "González López"
        alumno2.nrodocumento = "36234567"
        alumno2.tipo_documento = dni
        alumno2.nro_legajo = 2024002
        alumno2.especialidad = especialidad1

        alumno3 = Alumno()
        alumno3.id = 3
        alumno3.nombre = "Carlos"
        alumno3.apellido = "Martínez Ruiz"
        alumno3.nrodocumento = "37345678"
        alumno3.tipo_documento = dni
        alumno3.nro_legajo = 2024003
        alumno3.especialidad = especialidad2

        AlumnoRepository._alumnos = [alumno1, alumno2, alumno3]
        AlumnoRepository._next_id = 4
