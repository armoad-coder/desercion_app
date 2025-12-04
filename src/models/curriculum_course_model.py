from src.utils.extensions import db

class CurriculumCourse(db.Model):
    __tablename__ = 'curriculum_courses'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Claves Foráneas
    carrera_id = db.Column(db.Integer, db.ForeignKey('majors.id'), nullable=False)
    materia_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    semestre_id = db.Column(db.Integer, db.ForeignKey('semesters.id'), nullable=False)
    
    # Evitar duplicados: Una materia no puede estar dos veces en el mismo semestre de la misma carrera
    __table_args__ = (
        db.UniqueConstraint('carrera_id', 'materia_id', 'semestre_id', name='_curriculum_uc'),
    )