from flask import Blueprint, jsonify, request
from modelos.medico import obtener_medicos,obtener_medico_por_id,crear_medico,actualizar_medico_por_id


# Creamos el blueprint
medicos_bp = Blueprint('medicos', __name__)

#---------------------------------------GET Medicos-----------------------------------------------------

@medicos_bp.route('/medicos', methods=['GET'])
def obtener_medicos_json():
    try:
        medicos = obtener_medicos()

        if not medicos:
            return jsonify({"error": "No hay médicos disponibles"}), 404

        return jsonify(medicos), 200
    except Exception as e:
        return jsonify({"error": f"Error en el servidor: {str(e)}"}), 500


#----------------------------------------GET Medico Por ID------------------------------------------------

@medicos_bp.route('/medicos/<int:id_medico>', methods=["GET"])
def obtener_medico_por_id_json(id_medico):
    try:
        medico = obtener_medico_por_id(id_medico)
        
        if not medico:
            return jsonify({"error": "No existe un médico con ese ID"}), 404
        return jsonify(medico), 200
    except Exception as e:
        return jsonify({"error": f"Error en el servidor: {str(e)}"}), 500



#----------------------------------------POST Medico------------------------------------------------------
    
@medicos_bp.route('/medicos/', methods=["POST"])
def crear_medico_json():
    try:
        data = request.get_json()

        # Valida que se proporcionen todos los campos requeridos
        campos_requeridos = ["dni", "nombre", "apellido", "matricula", "telefono", "email", "habilitado"]
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

        # Valida que la matrícula tenga exactamente 6 dígitos
        matricula = str(data["matricula"])
        if not (matricula.isdigit() and len(matricula) == 6):
            return jsonify({"error": "La matrícula debe ser un número entero de 6 dígitos"}), 400

        # Valida que el teléfono tenga exactamente 9 dígitos
        telefono = data["telefono"]
        if not (telefono.isdigit() and len(telefono) == 9):
            return jsonify({"error": "El teléfono debe ser un número entero de 9 dígitos"}), 400

        # Valida que el email contenga al menos un '@'
        email = data["email"]
        if '@' not in email:
            return jsonify({"error": "El email debe contener al menos un '@'"}), 400
        
        # Valida que el email sea válido
        habilitado = data.get("habilitado", "true").lower()
        if habilitado not in ["true", "false"]:
            return jsonify({"error": "El valor de 'habilitado' debe ser 'True' o 'False'"}), 400

        # Valida que no exista el medico
        medicos_existentes = obtener_medicos()
        for medico_existente in medicos_existentes:
            if (medico_existente["dni"] == dni 
                    or medico_existente["matricula"] == matricula 
                    or (medico_existente["nombre"].lower() == nombre.lower()
                    and medico_existente["apellido"].lower() == apellido.lower())):
                return jsonify({"error": "Ya existe un médico con el mismo DNI, matrícula, nombre o apellido"}), 400

        medico_creado = crear_medico(dni, nombre, apellido, matricula, telefono, email, habilitado)
        return jsonify(medico_creado), 201

    except KeyError:
        return jsonify({"error": "Faltan datos"}), 400
    except Exception as e:
        return jsonify({"error": f"Error en el servidor: {str(e)}"}), 500


    
#-------------------------------------------PUT Medico---------------------------------------------------

@medicos_bp.route('/medicos/<int:id_medico>', methods=["PUT"])
def actualizar_medico_json(id_medico):
    try:
        data = request.get_json()
        # Valida que el médico exista
        medico_existente = obtener_medico_por_id(id_medico)
        if not medico_existente:
            return jsonify({"error": "Médico no encontrado"}), 404

        # Valida que se proporcionen todos los campos requeridos
        campos_requeridos = ["dni", "nombre", "apellido", "matricula", "telefono", "email", "habilitado"]
        for campo in campos_requeridos:
            if campo not in data:
                return jsonify({"error": f"Falta el campo '{campo}'"}), 400

        # Valida que el DNI sea un número entero de 8 dígitos
        dni = data["dni"]
        if not (dni.isdigit() and len(dni) == 8):
            return jsonify({"error": "El DNI debe ser un número entero de 8 dígitos"}), 400

        # Valida que el nombre y el apellido no sean cadenas vacías y solo contengan letras
        nombre = data["nombre"]
        apellido = data["apellido"]
        if not (nombre.isalpha() and apellido.isalpha()):
            return jsonify({"error": "El nombre y el apellido deben contener solo letras y no estar vacíos"}), 400

        # Valida que la matrícula tenga exactamente 6 dígitos
        matricula = str(data["matricula"])
        if not (matricula.isdigit() and len(matricula) == 6):
            return jsonify({"error": "La matrícula debe ser un número entero de 6 dígitos"}), 400

        # Valida que el teléfono tenga exactamente 9 dígitos
        telefono = data["telefono"]
        if not (telefono.isdigit() and len(telefono) == 9):
            return jsonify({"error": "El teléfono debe ser un número entero de 9 dígitos"}), 400

        # Valida que el email contenga al menos un '@'
        email = data["email"]
        if '@' not in email:
            return jsonify({"error": "El email debe contener al menos un '@'"}), 400
        
        # Valida que el email sea válido
        habilitado = data.get("habilitado", "true").lower()
        if habilitado not in ["true", "false"]:
            return jsonify({"error": "El valor de 'habilitado' debe ser 'True' o 'False'"}), 400

        # Valida que no exista el medico
        medicos_existentes = obtener_medicos()
        for medico_existente in medicos_existentes:
            if ((medico_existente["dni"] == dni 
                    or medico_existente["matricula"] == matricula 
                    or (medico_existente["nombre"].lower() == nombre.lower()
                    and medico_existente["apellido"].lower() == apellido.lower())))and medico_existente["id"]!= id_medico:
                return jsonify({"error": "Ya existe un médico con el mismo DNI, matrícula, nombre o apellido"}), 400

        medico_modificado = actualizar_medico_por_id(id_medico,dni,nombre,apellido,matricula,telefono,email,habilitado)
                                                    
        return jsonify(medico_modificado), 200
    except KeyError:
        return jsonify({"error": "Faltan datos"}), 400
    except Exception as e:
        return jsonify({"error": f"Error en el servidor: {str(e)}"}), 500




#----------------------------------------------------------------------------------------------