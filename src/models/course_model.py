from src.utils.extensions import db

class Course(db.Model):
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False) # Ej: "Cálculo I"
    codigo = db.Column(db.String(20), nullable=False, unique=True) # Ej: "MAT-101"
    
    def __repr__(self):
        return f'<Course {self.nombre}>'