from datetime import datetime

from flask import Blueprint, jsonify, request
from modelos.agenda_medico import obtener_agenda_medicos,obtener_agenda_medico_por_id,crear_agenda_medico,eliminar_dia_agenda_medico_por_id,actualizar_agenda_por_dia,obtener_agenda_ordenada_medicos


# Creamos el blueprint
agenda_medicos_bp = Blueprint('agenda', __name__)

#-------------------------------------------------GET Agenda Completa -------------------------------------------------

@agenda_medicos_bp.route('/agenda', methods=['GET'])
def obtener_agenda_medicos_json():
    try:
        #obtener agenda
        agenda = obtener_agenda_ordenada_medicos()
        if not agenda:
            return jsonify({"error":"No hay agendas medicas"}), 404
        return jsonify(agenda), 200
    except Exception as e:
        return jsonify({"error":f"Error en el servidor: {str(e)}"})

#-------------------------------------------------GET Agenda por ID Medico -------------------------------------------------

@agenda_medicos_bp.route('/agenda/<int:id_medico>', methods=["GET"])
def obtener_agenda_medico_por_id_json(id_medico):
    try:
        #obtener agenda por id
        medico = obtener_agenda_medico_por_id(id_medico)
        if medico:
            return jsonify(medico), 200
        else:
            return jsonify({"error":"Medico no encontrado"}), 404
    except Exception as e:
        return jsonify({"error":f"Error en el servidor: {str(e)}"}), 500
    

#-------------------------------------------------POST Agenda de Un Medico -------------------------------------------------

@agenda_medicos_bp.route('/agenda/<int:id_medico>', methods=["POST"])
def crear_agenda_medico_json(id_medico):
    try:
        # Verificar si el médico existe
        medico_existente = obtener_agenda_medico_por_id(id_medico)
        if medico_existente is None:
            return jsonify({"error": "Médico no encontrado"}), 404

        # Obtener datos del cuerpo de la solicitud en formato JSON
        data = request.get_json()

        # Validar que se proporcionen todos los campos requeridos
        campos_requeridos = ["dia_numero", "hora_inicio", "hora_fin"]
        for campo in campos_requeridos:
            if campo not in data:
                return jsonify({"error": f"Falta el campo '{campo}'"}), 400

        # Validar que el valor de 'dia_numero' esté entre 0 y 6
        dia_numero = data["dia_numero"]
        if not (isinstance(dia_numero, int) and 0 <= dia_numero <= 6):
            return jsonify({"error": "El valor de 'dia_numero' debe estar entre 0 y 6"}), 400
        
        
        agenda_medico = obtener_agenda_medico_por_id(id_medico)
        for medico in agenda_medico:
            if medico["dia_numero"] == dia_numero:
                return jsonify({"error":"Ese dia ya esta agendado"})
       
       
        hora_inicio= data["hora_inicio"]
        hora_fin= data["hora_fin"]
        try:
            hora_inicio_str = datetime.strptime(hora_inicio, "%H:%M")
            hora_fin_str = datetime.strptime(hora_fin, "%H:%M")
        except ValueError:
            errores.append("El formato de hora no es válido. Debe ser en formato HH:MM")

        # Crear un nuevo día en la agenda del médico
        agenda_medico_creado = crear_agenda_medico(id_medico, dia_numero, hora_inicio, hora_fin)
        return jsonify(agenda_medico_creado), 201

    except KeyError:
        return jsonify({"error": "Faltan datos"}), 400
    except Exception as e:
        return jsonify({"error": f"Error en el servidor: {str(e)}"}), 500

    
#-------------------------------------------------DELETE Dia de Agenda de un Medico  -------------------------------------------------
    
@agenda_medicos_bp.route('/agenda/<int:id_medico>/<int:dia_numero>', methods=["DELETE"])
def eliminar_dia_agenda_medico_json(id_medico, dia_numero):
    try:
        # Verifica si el médico existe
        medico_existente = obtener_agenda_medico_por_id(id_medico)
        if medico_existente is None:
            return jsonify({"error": "Médico no encontrado"}), 404

        # Valida que el valor de 'dia_numero' esté en el rango correcto (0-6)
        if not (isinstance(dia_numero, int) and 0 <= dia_numero <= 6):
            return jsonify({"error": "El valor de 'dia_numero' debe estar entre 0 y 6"}), 400

        # Elimina el día específico de la agenda del médico
        dia_eliminado = eliminar_dia_agenda_medico_por_id(id_medico, dia_numero)
        if dia_eliminado:
            mensaje = {"message": f"Día {dia_numero} eliminado correctamente de la Agenda del Médico {id_medico}"}
            return jsonify(mensaje), 200
        else:
            mensaje = {"error": f"Día {dia_numero} no encontrado en la Agenda del Médico {id_medico}"}
            return jsonify(mensaje), 404

    except Exception as e:
        return jsonify({"error": f"Error en el servidor: {str(e)}"}), 500
    
#-------------------------------------------------PUT Agenda de un Medico -------------------------------------------------
    
@agenda_medicos_bp.route('/agenda/<int:id_medico>', methods=["PUT"])
def actualizar_agenda_medico_json(id_medico):
    try:
        # Verifica si el médico existe
        medico_existente = obtener_agenda_medico_por_id(id_medico)
        if medico_existente is None:
            return jsonify({"error": "Médico no encontrado"}), 404
        
        lista_data = []
        lista_data = request.get_json()
        
        errores = []
       
        for data in lista_data:
            # Verifica la presencia de campos requeridos en cada conjunto de datos
            campos_requeridos = ["dia_numero", "hora_inicio", "hora_fin"]
            for campo in campos_requeridos:
                if campo not in data:
                    errores.append(f"Falta el campo '{campo}' para el conjunto de datos {data}")

            if errores:
                return jsonify({"errores": errores}), 400

            # Valida que el valor de 'dia_numero' esté en el rango correcto (0-6)
            dia_numero = data.get("dia_numero")
            if not (isinstance(dia_numero, int) and 0 <= dia_numero <= 6):
                errores.append("El valor de 'dia_numero' debe estar entre 0 y 6")

            # Valida el formato de las horas proporcionadas
            hora_inicio = data["hora_inicio"]
            hora_fin = data["hora_fin"]
            try:
                hora_inicio_str = datetime.strptime(hora_inicio, "%H:%M")
                hora_fin_str = datetime.strptime(hora_fin, "%H:%M")
            except ValueError:
                errores.append("El formato de hora no es válido. Debe ser en formato HH:MM")

            # Si no hay errores, actualiza la agenda para el día especificado
            if not errores:
                agenda_actualizada = actualizar_agenda_por_dia(id_medico, dia_numero, hora_inicio, hora_fin)      
                if agenda_actualizada:
                    agenda_med = obtener_agenda_medico_por_id(id_medico)
                    return jsonify(agenda_med), 200
                else:
                    return jsonify({"error": "No se pudo actualizar la agenda"}), 404

    except Exception as e:
        return jsonify({"error": f"Error en la solicitud: {str(e)}"}), 500



