from src.utils.extensions import db

class AcademicRecord(db.Model):
    __tablename__ = 'academic_records'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Datos de rendimiento
    nota = db.Column(db.Float, nullable=False)
    ausencias = db.Column(db.Integer, nullable=False, default=0)
    estatus_final = db.Column(db.String(50), nullable=False) # Aprobado, Reprobado, Retirado
    
    # Claves Foráneas (Quién, Qué, Cuándo)
    alumno_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    materia_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    año_id = db.Column(db.Integer, db.ForeignKey('academic_years.id'), nullable=False)
    semestre_id = db.Column(db.Integer, db.ForeignKey('semesters.id'), nullable=False)

    # NUEVO CAMPO: Tipo de Evaluación (ORD, 1EF, 2ORD, COMPLE)
    evaluation_type_id = db.Column(db.Integer, db.ForeignKey('evaluation_types.id'), nullable=False)
    
# Un alumno solo puede tener UNA nota por Materia + Año + Semestre + TIPO DE EVALUACIÓN
    __table_args__ = (
        db.UniqueConstraint(
            'alumno_id', 
            'materia_id', 
            'año_id', 
            'semestre_id', 
            'evaluation_type_id', # Agregamos esto a la llave única
            name='_record_evaluation_uc'
        ),
    )