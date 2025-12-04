from flask import Flask
from src.utils.configs import Config
from flask_migrate import Migrate
from src.utils.extensions import db, bcrypt, jwt, cors
from src.routes.user_routes import user_bp
from src.routes.auth_routes import auth_bp

def create_app():
    app = Flask(__name__)
    # Importamos la configuración de conexión a la BD desde configs.py 
    app.config.from_object(Config)

    # Inicializamos extenciones en el proyecto.
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)

    # === MODELOS DE BASE DE DATOS ===
    # Importar modelos para que Migrate los detecte(No son utilizados en app.py como tal)
    from src.models.user_models import User
    # Catálogos Básicos (Definiciones)
    from src.models.academic_year_model import AcademicYear
    from src.models.semester_model import Semester
    from src.models.major_model import Major
    from src.models.course_model import Course
    from src.models.evaluation_type_model import EvaluationType

    # Entidades Principales
    from src.models.student_model import Student

    # Tablas de Relación (Uniones)
    from src.models.curriculum_model import CurriculumCourse
    from src.models.academic_record_model import AcademicRecord

    # Registramos los blueprint para routes.
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    # Para migraciones
    Migrate(app, db)
    return app
    
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)