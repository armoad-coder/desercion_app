# src/routes/data_loading_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt

# Importa los servicios de loading
from src.services.data_loading_service import (
    load_major_data,
    load_academic_year_data,
    load_semester_data,
    load_course_data
)
# Importa tu función de verificación de rol (asumo que está en common_utils o similar)
# from src.utils.common_utils import is_admin 

data_bp = Blueprint('data_loading', __name__, url_prefix='/api/data')

# Nota: Asumimos que tienes una función is_admin o un decorador similar 
# para validar si el rol dentro del JWT es 'admin'.

@data_bp.route('/load_majors', methods=['POST'])
# @is_admin # Aquí iría tu decorador de protección de rol
def load_majors():
    # Obtener el rol del usuario para la verificación (de forma básica)
    # user_role = get_jwt().get("role")
    # if user_role != 'admin':
    #     return jsonify({"msg": "Acceso denegado: solo administradores"}), 403

    data = request.get_json()
    if not isinstance(data, list):
        return jsonify({"error": "El cuerpo debe ser una lista de objetos JSON"}), 400

    results = load_major_data(data)
    
    return jsonify({
        "message": f"Proceso de carga de {len(results)} registros completado.",
        "details": results
    }), 200

@data_bp.route('/load_academic_years', methods=['POST'])
# @is_admin # Aquí iría tu decorador de protección de rol
def load_academic_years():
    data = request.get_json()
    print(data)
    if not isinstance(data, list):
        return jsonify({"error": "El cuerpo debe ser una lista de objetos JSON"}), 400

    results = load_academic_year_data(data)
    
    return jsonify({
        "message": f"Proceso de carga de Años Académicos completado. ({len(results)} registros procesados).",
        "details": results
    }), 200

@data_bp.route('/load_semesters', methods=['POST'])
# @is_admin 
def load_semesters():
    data = request.get_json()
    if not isinstance(data, list):
        return jsonify({"error": "El cuerpo debe ser una lista de objetos JSON"}), 400

    results = load_semester_data(data)
    
    return jsonify({
        "message": f"Proceso de carga de Semestres completado. ({len(results)} registros procesados).",
        "details": results
    }), 200

@data_bp.route('/load_courses', methods=['POST'])
# @is_admin 
def load_courses():
    data = request.get_json()
    if not isinstance(data, list):
        return jsonify({"error": "El cuerpo debe ser una lista de objetos JSON"}), 400

    results = load_course_data(data)
    
    return jsonify({
        "message": f"Proceso de carga de Materias completado. ({len(results)} registros procesados).",
        "details": results
    }), 200