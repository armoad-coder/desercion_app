# src/services/data_loading_service.py
from src.utils.extensions import db
from src.models.major_model import Major
from src.models.academic_year_model import AcademicYear
from src.models.semester_model import Semester
from src.models.course_model import Course
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