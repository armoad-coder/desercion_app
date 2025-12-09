# src/models/academic_record_model.py
from src.utils.extensions import db

class AcademicRecord(db.Model):
    __tablename__ = 'academic_records'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Datos de rendimiento
    nota = db.Column(db.Float, nullable=False) # NOTA: Valor numérico (ej. 5.0)
    
    # Bandera de distinción: True si la nota fue un 5F (100%)
    is_cinco_felicitado = db.Column(db.Boolean, default=False, nullable=False)
    
    ausencias = db.Column(db.Integer, nullable=False, default=0)
    estatus_final = db.Column(db.String(50), nullable=False) 
    
    # Claves Foráneas (Se mantienen)
    alumno_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    materia_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    año_id = db.Column(db.Integer, db.ForeignKey('academic_years.id'), nullable=False)
    semestre_id = db.Column(db.Integer, db.ForeignKey('semesters.id'), nullable=False)
    evaluation_type_id = db.Column(db.Integer, db.ForeignKey('evaluation_types.id'), nullable=False)
    
    # Restricción Única (Se mantiene)
    __table_args__ = (
        db.UniqueConstraint(
            'alumno_id', 
            'materia_id', 
            'año_id', 
            'semestre_id', 
            'evaluation_type_id', 
            name='_record_evaluation_uc'
        ),
    )