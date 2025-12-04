from flask import Blueprint, request, jsonify
from src.services.auth_services import login_service

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No se enviaron datos'}), 400

    try:
        result = login_service(data)
        
        # Si login_service no lanza error, es exitoso
        return jsonify({
            'message': 'Login exitoso',
            'token': result['access_token'],
            'user': result['user']
        }), 200

    except ValueError as e:
        # Capturamos "Credenciales inválidas" o "Faltan datos"
        return jsonify({'error': str(e)}), 401
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor'}), 500