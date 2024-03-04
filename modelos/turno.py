# -----------------------------------------------------------------
# Módulo de funciones sobre Turnos
# -----------------------------------------------------------------

# Importaciones necesarias
from flask import Blueprint, jsonify, request
from datetime import datetime
import requests
import csv
import os

# Variables globales
turnos = []  # Lista que almacena los turnos

ruta_archivo_turnos = 'modelos\\turnos.csv'

#----------------------------------------------------------------------------------------------

# Función para importar datos de turnos desde un archivo CSV
def importar_datos_turnos_desde_csv():
    global turnos    
    if os.path.exists(ruta_archivo_turnos):  
        print("Importando datos de turnos desde el archivo CSV")
        turnos = []  # Limpiamos la lista de turnos antes de importar desde el archivo CSV
        with open(ruta_archivo_turnos, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Convertimos el ID de cadena a entero
                row['id_medico'] = int(row['id_medico'])
                row['id_paciente'] = int(row['id_paciente'])
                turnos.append(row) 
    else:
        print("No existe el archivo de turnos, creando..")
        turnos = []  
        exportar_a_csv()
        

#----------------------------------------------------------------------------------------------  

# Función para exportar datos de turnos a un archivo CSV
def exportar_a_csv():
    with open(ruta_archivo_turnos, 'w', newline='', encoding='utf-8') as csvfile:
        campo_nombres = ['id_medico', 'id_paciente', 'hora_turno', 'fecha_solicitud']
        writer = csv.DictWriter(csvfile, fieldnames=campo_nombres)
        writer.writeheader()
        for turno in turnos:
            writer.writerow(turno)
        
#----------------------------------------------------------------------------------------------

# Función para obtener los turnos de un médico por su ID
def obtener_turno_por_id_medico(id_medico):
    turnos_medico = []
    for turno in turnos:
        if turno["id_medico"] == id_medico:
            turnos_medico.append(turno)
    return turnos_medico

#----------------------------------------------------------------------------------------------

# Función para obtener los turnos pendientes de un médico por su ID
def obtener_turno_pendiente_por_id(id_medico):
    turnos_pendientes = []
    hoy = datetime.now()

    for turno in turnos:
        # Convertir la fecha y hora del turno a objetos datetime
        fecha_turno_dt = datetime.strptime(turno["fecha_solicitud"] + " " + turno["hora_turno"], "%d-%m-%Y %H:%M")

        # Verificar si la fecha es superior a la fecha actual
        if fecha_turno_dt.date() > hoy.date():
            turnos_pendientes.append(turno)
        # Si la fecha es la misma que la fecha actual, verificar la hora
        elif fecha_turno_dt.date() == hoy.date() and fecha_turno_dt.time() > hoy.time():
            turnos_pendientes.append(turno)

    return turnos_pendientes
#----------------------------------------------------------------------------------------------

# Función para eliminar un turno por su ID de médico y paciente
def eliminar_turno_por_id(id_medico, id_paciente):
    global turnos
    aux_turnos = list(turnos) 
    turnos = [turno for turno in turnos if not (turno["id_medico"] == id_medico and turno["id_paciente"] == id_paciente)]
    if len(turnos) < len(aux_turnos):
        exportar_a_csv()
        return True
    else:
        return False
    
#----------------------------------------------------------------------------------------------
 
# Función para crear un nuevo turno
def crear_turno(id_medico, id_paciente, fecha_turno, hora_turno):
    global turnos
    
    turno_medico = obtener_turno_por_id_medico(id_medico)
    
    if not any(turno["id_paciente"] == id_paciente for turno in turno_medico):
        nuevo_turno = {
            "id_medico": id_medico,
            "id_paciente": id_paciente,
            "fecha_solicitud": fecha_turno,
            "hora_turno": hora_turno
        }
        turnos.append(nuevo_turno)
        exportar_a_csv()
        return True, {"message": "Turno creado correctamente"}
    else: 
        return False, {"error": "El paciente ya tiene un turno con el médico"}

#----------------------------------------------------------------------------------------------
       
# Función para obtener los turnos de un paciente por su ID
def obtener_turno_por_paciente(id_paciente):
    turnos_paciente = []
    for turno in turnos:
        if turno["id_paciente"] == id_paciente:
            turnos_paciente.append(turno)
    return turnos_paciente

#----------------------------------------------------------------------------------------------

def obtener_turno_dado(id_medico, hora_turno, fecha_turno):
    for turno in turnos:
        if turno["id_medico"] == id_medico and turno["hora_turno"] == hora_turno and turno["fecha_solicitud"] == fecha_turno:
            return True
    return False

#----------------------------------------------------------------------------------------------

def obtener_paciente_turno(id_medico, id_paciente, hora_turno, fecha_turno):
    hoy = datetime.now()
    hora_actual = hoy.strftime("%H:%M")

    for turno in turnos:
        # Convertir las cadenas a objetos datetime
        fecha_solicitud_dt = datetime.strptime(turno["fecha_solicitud"], "%d-%m-%Y")
        hora_turno_dt = datetime.strptime(turno["hora_turno"], "%H:%M")

        # Comparar las fechas y horas
        if (
            turno["id_medico"] == id_medico
            and turno["id_paciente"] == id_paciente
            and (fecha_solicitud_dt.date() > hoy.date() or hora_turno_dt.time() > hoy.time())
        ):
            return turno

    return None


