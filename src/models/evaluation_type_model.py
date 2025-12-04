# src/models/evaluation_type_model.py
from src.utils.extensions import db

class EvaluationType(db.Model):
    __tablename__ = 'evaluation_types'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False) # Ej: "Examen Ordinario"
    codigo = db.Column(db.String(10), nullable=False, unique=True) # Ej: "ORD", "EXT"
    
    def __repr__(self):
        return f'<EvaluationType {self.codigo}>'