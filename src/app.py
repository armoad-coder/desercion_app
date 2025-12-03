from flask import Flask
from utils.configs import Config
from flask_migrate import Migrate
from utils.extensions import db, bcrypt, jwt, cors
from routes.user_routes import user_bp
from routes.auth_routes import auth_bp

def create_app():
    app = Flask(__name__)
    # Importamos la configuración de conexión a la BD desde configs.py 
    app.config.from_object(Config)

    # Inicializamos extenciones en el proyecto.
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)

    # Importar modelos para que Migrate los detecte(No son utilizados en app.py como tal)
    from models.user_models import User

    # Registramos los blueprint para routes.
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    # Para migraciones
    Migrate(app, db)
    return app
    
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)