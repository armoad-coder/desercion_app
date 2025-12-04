# Archivo: seed.py
from run import create_app
from src.utils.extensions import db
from src.models.user_models import User

app = create_app()

def create_admin():
    with app.app_context():
        # Crear tablas si no existen
        db.create_all()

        # Datos del Super Admin
        admin_email = "admin@sistema.com"
        admin_pass = "admin1234" # ¡Cámbiala después!

        # Verificar si ya existe para no duplicar
        if User.query.filter_by(email=admin_email).first():
            print(f"El usuario {admin_email} ya existe.")
            return

        # Crear usuario
        admin = User(
            email=admin_email,
            nombre="Super",
            apellido="Admin"
        )
        admin.set_password(admin_pass)

        db.session.add(admin)
        db.session.commit()
        print(f"¡Éxito! Usuario creado: {admin_email} / Password: {admin_pass}")

if __name__ == "__main__":
    create_admin()