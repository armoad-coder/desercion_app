from src.models.user_models import User
from flask_jwt_extended import create_access_token

def login_service(data):
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        raise ValueError("Se requiere email y contraseña.")

    # Buscamos al usuario
    user = User.query.filter_by(email=email).first()

    # Validamos usuario y contraseña
    # Usamos el método check_password que definiste en el modelo
    if user and user.check_password(password):
        
        # Generamos el token JWT
        # 'identity' suele ser el ID del usuario. Lo convertimos a string por compatibilidad.
        access_token = create_access_token(identity=str(user.id))

        return {
            'access_token': access_token,
            'user': {
                'id': user.id,
                'email': user.email,
                'nombre': user.nombre,
                'apellido': user.apellido
            }
        }
    
    # Si falla algo, lanzamos error o retornamos None
    raise ValueError("Credenciales inválidas.")