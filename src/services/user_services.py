from utils.extensions import db
from models.user_models import User

# Crear User.
def create_user_service(data):
    email = data.get('email')
    password = data.get('password')
    nombre = data.get('nombre')
    apellido = data.get('apellido')

    # 1. Validación de negocio: Verificar si el email ya existe
    if User.query.filter_by(email=email).first():
        raise ValueError('El email ya está registrado.')

    # 2. Crear la instancia del usuario
    new_user = User(
        email=email,
        nombre=nombre,
        apellido=apellido
    )

    # 3. Encriptar la contraseña
    # Usamos el método helper que creaste en el modelo User
    new_user.set_password(password)

    # 4. Persistencia en Base de Datos
    try:
        db.session.add(new_user)
        db.session.commit()
        return new_user
    except Exception as e:
        # Es buena práctica hacer rollback si algo falla en la transacción
        db.session.rollback()
        raise e

# Modificar User
def update_user_service(user_id, data):
    user = User.query.get(user_id)
    if 'password' in data:
        raise ValueError('La contraseña no puede ser modificada aquí. Está operacion se realiza en /reset_password.')
    if not user:
        return None # O lanzar una excepción específica de "No encontrado"

    # Actualización de Email con validación extra
    # Si cambian el email, debemos verificar que el nuevo no esté ocupado por otro usuario
    new_email = data.get('email')
    if new_email and new_email != user.email:
        existing_user = User.query.filter_by(email=new_email).first()
        if existing_user:
            raise ValueError('El nuevo email ya está en uso por otro usuario.')
        user.email = new_email

    # Actualizamos nombre y apellido
    # Usamos .get(campo, valor_actual) para mantener el dato viejo si no envían el nuevo
    user.nombre = data.get('nombre', user.nombre)
    user.apellido = data.get('apellido', user.apellido)

    # Nota: NO tocamos user.password aquí.

    try:
        db.session.commit()
        return user
    except Exception as e:
        db.session.rollback()
        raise e

# reset de password.
# ... importaciones existentes (db, User) ...

def reset_password_service(user_id, data):
    user = User.query.get(user_id)
    if not user:
        return None  # Usuario no encontrado

    old_password = data.get('old_password')
    new_password = data.get('new_password')
    reply_password = data.get('reply_password')

    # Validación 1: Campos obligatorios
    if not old_password or not new_password or not reply_password:
        raise ValueError('Se requieren la contraseña actual, la nueva contraseña y repetir la contraseña.')

    # Validación 2: Verificar que la contraseña antigua sea correcta
    if not user.check_password(old_password):
        raise ValueError('La contraseña actual es incorrecta.')

    # Validación 3 (Opcional): Que la nueva no sea igual a la vieja
    if old_password == new_password:
        raise ValueError('La nueva contraseña debe ser diferente a la actual.')
    # Validamos que new_password sea igual a reply_password.
    if new_password != reply_password:
        raise ValueError('Las contraseñas nuevas no coinciden.')

    # Procedemos al cambio
    user.set_password(new_password)

    try:
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        raise e