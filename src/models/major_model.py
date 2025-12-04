from src.utils.extensions import db

class Major(db.Model):
    __tablename__ = 'majors'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True) # Ej: "Ingeniería Informática"
    codigo = db.Column(db.String(20), nullable=False, unique=True) # Ej: "INF"
    
    def __repr__(self):
        return f'<Major {self.nombre}>'