from src.utils.extensions import db

class Semester(db.Model):
    __tablename__ = 'semesters'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True) # Ej: "1er Semestre"
    semestre = db.Column(db.Integer, nullable=False) # Ej: 1

    def __repr__(self):
        return f'<Semester {self.nombre}>'