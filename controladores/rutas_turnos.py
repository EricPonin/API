from flask import Blueprint, jsonify, request
from modelos.turno import obtener_turno_por_id_medico, obtener_turno_pendiente_por_id,eliminar_turno_por_id,crear_turno,obtener_turno_dado,obtener_paciente_turno
from modelos.medico import obtener_medico_por_id,obtener_medico_habilitado
from modelos.paciente import obtener_paciente_por_id
from modelos.agenda_medico import obtener_dia_agenda,obtener_hora_agenda

from datetime import datetime
hoy = datetime.now()

# Creamos el blueprint
turnos_bp = Blueprint('turnos', __name__)

#----------------------------------------------------------------------------------------------

# Obtener todos los turnos de un médico por su ID
@turnos_bp.route('/turnos/<int:id_medico>', methods=["GET"])
def obtener_turno_por_id_json(id_medico):
    try:
        # Obtener información del médico
        medico = obtener_medico_por_id(id_medico)
        if medico is None:
            return jsonify({"error" :"Médico no encontrado"}), 404

        # Obtener los turnos del médico por su ID
        turno = obtener_turno_por_id_medico(id_medico)
        if turno:
            return jsonify(turno), 200
        else:
            return jsonify({"error":"No hay turnos para este médico"}), 404
    except Exception as e:
        return jsonify({"error": f"Error en el servidor: {str(e)}"}), 500

#----------------------------------------------------------------------------------------------

# Obtener todos los turnos pendientes de un médico por su ID
@turnos_bp.route('/turnos/pendientes/<int:id_medico>', methods=["GET"])
def obtener_turno_pendiente_por_id_json(id_medico):
    try:
        # Obtener información del médico
        medico = obtener_medico_por_id(id_medico)
        if medico is None:
            return jsonify({"error" :"Médico no encontrado"}), 404

        # Obtener los turnos pendientes del médico por su ID
        turno = obtener_turno_pendiente_por_id(id_medico)
        if turno:
            return jsonify(turno), 200
        else:
            return jsonify({"error":"No hay turnos pendientes para este médico"}), 404
    except Exception as e:
        return jsonify({"error": f"Error en el servidor: {str(e)}"}), 500

#----------------------------------------------------------------------------------------------

# Eliminar un turno por el ID del médico y el ID del paciente
@turnos_bp.route('/turnos/<int:id_medico>/<int:id_paciente>', methods=["DELETE"])
def eliminar_turno_json(id_medico, id_paciente):
    try:
        # Obtener información del médico
        medico = obtener_medico_por_id(id_medico)
        if medico is None:
            return jsonify({"error" :"Médico no encontrado"}), 404

        # Obtener información del paciente
        paciente = obtener_paciente_por_id(id_paciente)
        if paciente is None:
            return jsonify({"error" :"Paciente no encontrado"}), 404

        # Eliminar el turno por el ID del médico y el ID del paciente
        turno_eliminado = eliminar_turno_por_id(id_medico, id_paciente)
        if turno_eliminado:
            return jsonify({"message": "Turno eliminado correctamente"}), 200
        else:
            return jsonify({"error": "Turno no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": f"Error en el servidor: {str(e)}"}), 500

#----------------------------------------------------------------------------------------------

#Crear un turno por el ID del médico y el ID del paciente
@turnos_bp.route('/turnos/<int:id_medico>/<int:id_paciente>', methods=["POST"])
def crear_turno_json(id_medico, id_paciente):
    try:
        # Obtener los datos del JSON enviado en la solicitud
        data = request.get_json()

        # Verificar si se proporcionan todos los campos requeridos
        campos_requeridos = ["fecha_turno", "hora_turno"]
        for campo in campos_requeridos:
            if campo not in data:
                return jsonify({"error": f"Falta el campo '{campo}'"}), 400

        # Obtener fecha y hora del turno desde el JSON
        fecha_turno = data["fecha_turno"]
        hora_turno = data["hora_turno"]

        # Obtener información del médico
        medico = obtener_medico_por_id(id_medico)
        if medico is None:
            return jsonify({"error": "Médico no encontrado"}), 404

        # Verificar si el médico está habilitado
        medico_habilitado = obtener_medico_habilitado(id_medico)
        if medico_habilitado is None:
            return jsonify({"error": "Médico no habilitado"}), 404

        # Obtener información del paciente
        paciente = obtener_paciente_por_id(id_paciente)
        if paciente is None:
            return jsonify({"error": "Paciente no encontrado"}), 404

        # Convertir la fecha del turno a un objeto de fecha
        try:
            fecha_t = datetime.strptime(fecha_turno, "%d-%m-%Y").date()
        except ValueError:
            return jsonify({"error": "Formato de fecha inválido. Debe ser 'día-mes-año'"}), 400

        # Verificar que la fecha del turno no sea anterior a la fecha actual
        if fecha_t < datetime.now().date():
            return jsonify({"error": "No se puede ingresar una fecha anterior al día de hoy"}), 400

        # Obtener información sobre el día y la hora de la agenda del médico
        dia_del_turno = obtener_dia_agenda(id_medico, fecha_turno)
        if dia_del_turno is None:
            return jsonify({"error": "El médico no atiende ese día"}), 400

        hora_del_turno = obtener_hora_agenda(id_medico, hora_turno)
        if hora_del_turno is None:
            return jsonify({"error": "El médico no atiende esa hora"}), 400

        # Convertir la hora del turno a un objeto de tiempo
        try:
            hora_turno_dt = datetime.strptime(hora_turno, "%H:%M")
        except ValueError:
            return jsonify({"error": "Formato de hora inválido. Debe ser 'Horas:Minutos'"}), 400

        # Verificar que la hora del turno esté en intervalos de 15 minutos
        if hora_turno_dt.minute % 15 != 0:
            return jsonify({"error": "La hora del turno debe estar en intervalos de 15 minutos"}), 400

        # Calcular la diferencia en días entre la fecha del turno y la fecha actual
        diferencia_dias = (fecha_t - hoy.date()).days
        if diferencia_dias > 30:
            return jsonify({"error": "Fecha inválida, el turno debe estar dentro de los próximos 30 días"}), 400
        
        turno_dado = obtener_turno_dado(id_medico, hora_turno, fecha_turno)
        if turno_dado:
            return jsonify({"error": "El medico ya tiene un turno a esa hora"})
        
        paciente_turno = obtener_paciente_turno(id_medico, id_paciente, hora_turno, fecha_turno)
        if paciente_turno:
            return jsonify({"error": "El paciente ya tiene un turno pendiente"})
        
        # Crear el turno y obtener el resultado
        creado, mensaje = crear_turno(id_medico, id_paciente, fecha_turno, hora_turno)
        if creado:
            return jsonify(mensaje), 200
        else:
            return jsonify(mensaje), 400
    except Exception as e:
        return jsonify({"error": f"Error en el servidor: {str(e)}"}), 500


    
    
