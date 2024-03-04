from flask import Blueprint, jsonify, request
from modelos.paciente import obtener_pacientes,obtener_paciente_por_id,crear_paciente,actualizar_paciente_por_id,eliminar_paciente_por_id,obtener_paciente_por_dni
from modelos.turno import obtener_turno_por_paciente

# Creamos el blueprint
pacientes_bp = Blueprint('pacientes', __name__)

#---------------------------------------GET Pacientes-------------------------------------------------------

@pacientes_bp.route('/pacientes', methods=['GET'])
def obtener_pacientes_json():
    try:
        pacientes = obtener_pacientes()

        if not pacientes:
            return jsonify({"error": "No hay pacientes disponibles"}), 404

        return jsonify(pacientes), 200

    except Exception as e:
        return jsonify({"error": f"Error en el servidor: {str(e)}"}), 500

#-------------------------------------GET Paciente Por ID---------------------------------------------------

@pacientes_bp.route('/pacientes/<int:id_paciente>', methods=["GET"])
def obtener_paciente_por_id_json(id_paciente):
    try:
        paciente = obtener_paciente_por_id(id_paciente)
        if not paciente:
            return jsonify({"error": "No existe un paciente con ese ID"}), 404
        return jsonify(paciente), 200
    except Exception as e:
        return jsonify({"error": f"Error en el servidor: {str(e)}"}), 500
        
    
#-------------------------------------POST Pacientes---------------------------------------------------------    

@pacientes_bp.route('/pacientes/', methods=["POST"])
def crear_paciente_json():
    try:
        data = request.get_json()

        # Valida que se proporcionen todos los campos requeridos
        campos_requeridos = ["dni", "nombre", "apellido", "telefono", "email", "dir_calle", "dir_numero"]
        for campo in campos_requeridos:
            if campo not in data:
                return jsonify({"error": f"Falta el campo '{campo}'"}), 400

        # Valida que el DNI sea un número entero de 10 dígitos
        dni = data["dni"]
        if not (dni.isdigit() and len(dni) == 8):
            return jsonify({"error": "El DNI debe ser un número entero de 8 dígitos"}), 400

        # Valida que el nombre y el apellido no sean cadenas vacías y solo contengan letras
        nombre = data["nombre"]
        apellido = data["apellido"]
        if not (nombre.isalpha() and apellido.isalpha()):
            return jsonify({"error": "El nombre y el apellido deben contener solo letras y no estar vacíos"}), 400

        # Valida que el teléfono tenga exactamente 9 dígitos
        telefono = data["telefono"]
        if not (telefono.isdigit() and len(telefono) == 9):
            return jsonify({"error": "El teléfono debe ser un número entero de 9 dígitos"}), 400

        # Valida que el email contenga al menos un '@'
        email = data["email"]
        if '@' not in email:
            return jsonify({"error": "El email debe contener al menos un '@'"}), 400
        
        # Valida que el campo 'dir_calle' no sea una cadena vacía
        dir_calle = data["dir_calle"]
        if not dir_calle:
            return jsonify({"error": "La calle de la dirección no puede estar vacía"}), 400

        # Valida que el campo 'dir_numero' sea un número entero positivo
        dir_numero = data["dir_numero"]
        if not (dir_numero.isdigit() and int(dir_numero) > 0):
            return jsonify({"error": "El número de dirección debe ser un número entero positivo"}), 400

        # Verifica si el paciente ya existe por DNI
        paciente_existente = obtener_paciente_por_dni(dni)
        if paciente_existente:
            return jsonify({"error": "Ya existe un paciente con este DNI"}), 409  # 409 conflicto

        paciente_creado = crear_paciente(dni, nombre, apellido, telefono, email, dir_calle, dir_numero)
        return jsonify(paciente_creado), 201  # 201 creado

    except KeyError:
        return jsonify({"error": "Faltan datos"}), 400
    except Exception as e:
        return jsonify({"error": f"Error en el servidor: {str(e)}"}), 500


    
#--------------------------------------PUT Pacientes--------------------------------------------------------    

@pacientes_bp.route('/pacientes/<int:id_paciente>', methods=["PUT"])
def actualizar_paciente_json(id_paciente):
    try:
        data = request.get_json()
        
        # Valida que el paciente exista
        paciente_existente = obtener_paciente_por_id(id_paciente)
        if not paciente_existente:
            return jsonify({"error": "Paciente no encontrado"}), 404

        # Valida que se proporcionen todos los campos requeridos
        campos_requeridos = ["dni", "nombre", "apellido", "telefono", "email", "dir_calle", "dir_numero"]
        for campo in campos_requeridos:
            if campo not in data:
                return jsonify({"error": f"Falta el campo '{campo}'"}), 400

        # Valida que el DNI sea un número entero de 10 dígitos
        dni = data["dni"]
        if not (dni.isdigit() and len(dni) == 8):
            return jsonify({"error": "El DNI debe ser un número entero de 8 dígitos"}), 400

        # Valida que el nombre y el apellido no sean cadenas vacías y solo contengan letras
        nombre = data["nombre"]
        apellido = data["apellido"]
        if not (nombre.isalpha() and apellido.isalpha()):
            return jsonify({"error": "El nombre y el apellido deben contener solo letras y no estar vacíos"}), 400

        # Valida que el teléfono tenga exactamente 9 dígitos
        telefono = data["telefono"]
        if not (telefono.isdigit() and len(telefono) == 9):
            return jsonify({"error": "El teléfono debe ser un número entero de 9 dígitos"}), 400

        # Valida que el email contenga al menos un '@'
        email = data["email"]
        if '@' not in email:
            return jsonify({"error": "El email debe contener al menos un '@'"}), 400
        
        # Valida que el campo 'dir_calle' no sea una cadena vacía
        dir_calle = data["dir_calle"]
        if not dir_calle:
            return jsonify({"error": "La calle de la dirección no puede estar vacía"}), 400

        # Valida que el campo 'dir_numero' sea un número entero positivo
        dir_numero = data["dir_numero"]
        if not (dir_numero.isdigit() and int(dir_numero) > 0):
            return jsonify({"error": "El número de dirección debe ser un número entero positivo"}), 400
        
        # Verifica si el paciente ya existe por DNI
        paciente_existente = obtener_paciente_por_dni(dni)
        if paciente_existente and paciente_existente["id"]!= id_paciente:
            return jsonify({"error": "Ya existe un paciente con este DNI"}), 409  # 409 conflicto

        paciente_modificado = actualizar_paciente_por_id(id_paciente, dni, nombre, apellido, telefono, email, dir_calle, dir_numero)
        return jsonify(paciente_modificado), 200
    except KeyError:
        return jsonify({"error": "Faltan datos"}), 400
    except Exception as e:
        return jsonify({"error": f"Error en el servidor: {str(e)}"}), 500

    
#------------------------------------DELETE Pacientes----------------------------------------------------------

@pacientes_bp.route('/pacientes/<int:id_paciente>', methods=["DELETE"])
def eliminar_paciente_json(id_paciente):
    paciente_con_turno= obtener_turno_por_paciente(id_paciente)
    if paciente_con_turno:
        return jsonify({"error": "Paciente tiene un turno asignado"}), 409  # 409 conflicto
    else:
        paciente_eliminado = eliminar_paciente_por_id(id_paciente)
        if paciente_eliminado:
            return jsonify({"message": "Paciente eliminado correctamente"}), 200
        else:
            return jsonify({"error": "Paciente no encontrado"}), 404