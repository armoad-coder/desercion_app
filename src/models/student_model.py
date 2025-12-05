from src.utils.extensions import db

class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    apellido = db.Column(db.String(80), nullable=False)
    sexo = db.Column(db.Integer, nullable=False)
    matricula = db.Column(db.String(50), unique=True, nullable=False)
    estado_actual = db.Column(db.String(20), default='Activo', nullable=False)

    # El alumno pertenece a una carrera
    carrera_id = db.Column(db.Integer, db.ForeignKey('majors.id'), nullable=False)

    # Año de ingreso
    ingreso_year_id = db.Column(db.Integer, db.ForeignKey('academic_years.id'), nullable=False)
    
    def __repr__(self):
        return f'<Student {self.matricula}>'