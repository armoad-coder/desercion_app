# src/services/data_loading_service.py
from src.utils.extensions import db
from src.models.major_model import Major
from src.models.academic_year_model import AcademicYear
from src.models.semester_model import Semester
from src.models.course_model import Course
from src.models.academic_record_model import AcademicRecord
from src.models.evaluation_type_model import EvaluationType 
from src.models.student_model import Student
from sqlalchemy.exc import IntegrityError


def load_major_data(data):
    """Procesa una lista de JSONs para cargar Carreras (Major)."""
    results = []
    
    for item in data:
        codigo = item.get('CODIGO')
        nombre = item.get('NOMBRE')
        
        if not codigo or not nombre:
            results.append({"error": "Faltan campos (CODIGO o NOMBRE)", "data": item})
            continue

        try:
            # 1. Intentar encontrar si ya existe por el código único
            major = Major.query.filter_by(codigo=codigo).first()
            
            if major:
                results.append({"status": "Skipped", "message": "Ya existe", "codigo": codigo})
            else:
                # 2. Si no existe, crear
                new_major = Major(nombre=nombre, codigo=codigo)
                db.session.add(new_major)
                db.session.commit()
                results.append({"status": "Created", "codigo": codigo})

        except IntegrityError:
            db.session.rollback()
            results.append({"error": "Error de integridad de datos", "codigo": codigo})
        except Exception as e:
            db.session.rollback()
            results.append({"error": str(e), "codigo": codigo})
            
    return results

def load_academic_year_data(data):
    """Procesa una lista de JSONs para cargar Años Académicos."""
    results = []
    
    for item in data:
        # Usamos 'año' como clave numérica única para la verificación
        year_num = item.get('AÑO')
        nombre = item.get('NOMBRE') 
        
        if not year_num or not nombre:
            results.append({"error": "Faltan campos (NOMBRE o AÑO)", "data": item})
            continue

        try:
            # 1. Intentar encontrar si ya existe por el campo único 'año'
            academic_year = AcademicYear.query.filter_by(año=year_num).first()
            
            if academic_year:
                results.append({"status": "Skipped", "message": "Ya existe", "año": year_num})
            else:
                # 2. Si no existe, crear
                new_year = AcademicYear(nombre=nombre, año=year_num)
                db.session.add(new_year)
                db.session.commit()
                results.append({"status": "Created", "año": year_num})

        except IntegrityError:
            db.session.rollback()
            results.append({"error": "Error de integridad de datos", "año": year_num})
        except Exception as e:
            db.session.rollback()
            results.append({"error": str(e), "año": year_num})
            
    return results

def load_semester_data(data):
    """Procesa una lista de JSONs para cargar Semestres."""
    results = []
    
    for item in data:
        # Recuperamos ambos valores: nombre y número
        semester_num = item.get('SEMESTRE') 
        nombre = item.get('NOMBRE')
        
        # Validación: ambos campos son necesarios para la creación
        if not nombre or semester_num is None: # Comprobamos si SEMESTRE es None
             results.append({"error": "Faltan campos (NOMBRE o SEMESTRE)", "data": item})
             continue

        try:
            # Buscamos por nombre, ya que es el campo único en el modelo
            semester = Semester.query.filter_by(nombre=nombre).first()
            
            if semester:
                results.append({"status": "Skipped", "message": "Ya existe", "nombre": nombre})
            else:
                # Si no existe, crear, incluyendo el número
                # ASUMIMOS QUE EL MODELO SEMESTER FUE CREADO CON UN CAMPO 'semestre'
                new_semester = Semester(
                    nombre=nombre, 
                    semestre=semester_num # <-- CORRECCIÓN: Usar el valor numérico
                ) 
                db.session.add(new_semester)
                db.session.commit()
                results.append({"status": "Created", "nombre": nombre})

        except IntegrityError:
            db.session.rollback()
            # Este error puede ocurrir si el 'semestre' numérico ya existe (si también es UNIQUE)
            results.append({"error": "Error de integridad de datos (posible duplicado)", "nombre": nombre})
        except Exception as e:
            db.session.rollback()
            results.append({"error": str(e), "nombre": nombre})
            
    return results

def load_course_data(data):
    """Procesa una lista de JSONs para cargar Materias (Course)."""
    results = []
    
    for item in data:
        codigo = item.get('CODIGO')
        nombre = item.get('NOMBRE') 
        
        if not codigo or not nombre:
            results.append({"error": "Faltan campos (CODIGO o NOMBRE)", "data": item})
            continue

        try:
            # 1. Buscar si ya existe por el campo único 'CODIGO'
            course = Course.query.filter_by(codigo=codigo).first()
            
            if course:
                results.append({"status": "Skipped", "message": "Ya existe", "codigo": codigo})
            else:
                # 2. Si no existe, crear
                new_course = Course(nombre=nombre, codigo=codigo)
                db.session.add(new_course)
                db.session.commit()
                results.append({"status": "Created", "codigo": codigo})

        except IntegrityError:
            db.session.rollback()
            results.append({"error": "Error de integridad de datos", "codigo": codigo})
        except Exception as e:
            db.session.rollback()
            results.append({"error": str(e), "codigo": codigo})
            
    return results

def load_student_data(data):
    """Procesa una lista de JSONs para cargar Alumnos (Student)."""
    results = []

    for item in data:
        # 🚨 NUEVO CAMPO: ID que viene de la fuente externa
        IDAlumno = item.get('IDALUMNO')
        matricula = item.get('MATRICULA')
        nombre = item.get('NOMBRE')
        apellido = item.get('APELLIDO')
        sexo = item.get('SEXO') 
        estado_actual = item.get('ESTADO_ACTUAL', 'Activo') 
        carrera_codigo = item.get('CARRERA_CODIGO')
        ingreso_year_num = item.get('INGRESO_ANIO') 
        
        # Validación de campos obligatorios (Añadimos IDALUMNO)
        if not all([IDAlumno, matricula, nombre, apellido, sexo, carrera_codigo, ingreso_year_num]):
            results.append({"error": "Faltan campos clave obligatorios (incluyendo IDALUMNO).", "data": item})
            continue

        try:
            # 1. Buscar IDs de las dependencias (se mantiene igual)
            carrera = Major.query.filter_by(codigo=carrera_codigo).first()
            ingreso_year = AcademicYear.query.filter_by(año=ingreso_year_num).first()

            # ... (verificaciones de catálogo se mantienen) ...
            if not carrera or not ingreso_year:
                # ... (error handling)
                continue

            # 2. Verificar existencia, ahora por el ID (PK)
            student = Student.query.get(IDAlumno)

            if student:
                results.append({"status": "Skipped", "message": "Alumno ya existe por IDALUMNO", "IDALUMNO": IDAlumno})
            else:
                # 3. Crear el nuevo estudiante, asignando ID manualmente
                new_student = Student(
                    id=IDAlumno,  # 🚨 ASIGNACIÓN DIRECTA DEL ID DE FUENTE
                    matricula=matricula,
                    nombre=nombre,
                    apellido=apellido,
                    sexo=sexo,
                    estado_actual=estado_actual,
                    carrera_id=carrera.id,
                    ingreso_year_id=ingreso_year.id
                )
                db.session.add(new_student)
                db.session.commit()
                results.append({"status": "Created", "IDALUMNO": IDAlumno})

        except IntegrityError:
            db.session.rollback()
            results.append({"error": "Error de integridad de datos (IDALUMNO o Matrícula duplicada)", "IDALUMNO": IDAlumno})
        except Exception as e:
            db.session.rollback()
            results.append({"error": str(e), "IDALUMNO": IDAlumno})
            
    return results

def _convert_nota_data(nota_codigo):
    """Convierte el código de nota ('5F', '5', etc.) a valor numérico y bandera 5F."""
    is_5f = False
    
    if nota_codigo == '5F':
        numeric_note = 5.0
        is_5f = True
    else:
        try:
            # Intenta convertir cualquier otro código (ej. '5', '4', '3') a float
            numeric_note = float(nota_codigo)
        except ValueError:
            # Si el código no es numérico (ej. 'APROBADO', 'REPROBADO'), asumimos 0.0
            numeric_note = 0.0 
            
    return numeric_note, is_5f # Devuelve la nota numérica y la bandera

# --- Función de Carga ---

def load_academic_record_data(data):
    """Procesa una lista de JSONs para cargar Registros Académicos (AcademicRecord)."""
    results = []

    for item in data:
        # Claves de búsqueda y datos a guardar (manteniendo el nombre del JSON)
        matricula = item.get('MATRICULA')
        materia_codigo = item.get('MATERIA_CODIGO')
        anio_num = item.get('ANIO_CURSADO')
        semestre_nombre = item.get('SEMESTRE_NOMBRE')
        evaluation_codigo = item.get('EVALUATION_CODIGO') 
        
        nota_codigo = item.get('NOTA_CODIGO_FUENTE') # e.g., '5F', '3', '1'
        ausencias = item.get('AUSENCIAS', 0)
        estatus_final = item.get('ESTATUS_FINAL', 'Sin definir')

        # 1. Validación de campos obligatorios
        if not all([matricula, materia_codigo, anio_num, semestre_nombre, evaluation_codigo, nota_codigo]):
            results.append({"error": "Faltan campos clave para el registro académico.", "data": item})
            continue

        try:
            # 2. Buscar IDs de las 5 dependencias (omitiendo la búsqueda de FKs para brevedad en este ejemplo)
            alumno = Student.query.filter_by(matricula=matricula).first()
            materia = Course.query.filter_by(codigo=materia_codigo).first()
            año = AcademicYear.query.filter_by(año=anio_num).first()
            semestre = Semester.query.filter_by(nombre=semestre_nombre).first()
            evaluation = EvaluationType.query.filter_by(codigo=evaluation_codigo).first()

            if not all([alumno, materia, año, semestre, evaluation]):
                results.append({"error": "No se encontró una o más entidades de catálogo.", "data": item})
                continue
            
            # 3. Conversion clave: obtiene nota numérica y el flag 5F
            nota_numerica, is_5f_flag = _convert_nota_data(nota_codigo)

            # 4. Verificar existencia (evitar duplicados)
            exists = AcademicRecord.query.filter_by(
                alumno_id=alumno.id,
                materia_id=materia.id,
                año_id=año.id,
                semestre_id=semestre.id,
                evaluation_type_id=evaluation.id
            ).first()

            if exists:
                results.append({"status": "Skipped", "message": "Registro académico ya existe", "matricula": matricula, "materia": materia_codigo})
            else:
                # 5. Crear el registro
                new_record = AcademicRecord(
                    alumno_id=alumno.id,
                    materia_id=materia.id,
                    año_id=año.id,
                    semestre_id=semestre.id,
                    evaluation_type_id=evaluation.id,
                    nota=nota_numerica, # <-- Campo numérico
                    is_cinco_felicitado=is_5f_flag, # <-- Flag para contar
                    ausencias=ausencias,
                    estatus_final=estatus_final
                )
                db.session.add(new_record)
                db.session.commit()
                results.append({"status": "Created", "matricula": matricula, "materia": materia_codigo})

        except IntegrityError:
            db.session.rollback()
            results.append({"error": "Error de integridad de datos (FK o clave única duplicada)", "data": item})
        except Exception as e:
            db.session.rollback()
            results.append({"error": str(e), "data": item})
            
    return results