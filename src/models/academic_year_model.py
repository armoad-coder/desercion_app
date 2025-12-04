from src.utils.extensions import db

class AcademicYear(db.Model):
    __tablename__ = 'academic_years'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True) # Ej: "2025"
    año = db.Column(db.Integer, nullable=False) # Ej: 2025
    
    def __repr__(self):
        return f'<AcademicYear {self.nombre}>'