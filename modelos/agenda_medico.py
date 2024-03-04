# -----------------------------------------------------------------
# Módulo de funciones sobre Agenda
# -----------------------------------------------------------------
from modelos.medico import obtener_medicos
from datetime import datetime , time
import requests
import csv
import os

# Variables globales que usaremos en este módulo
agenda = []
ruta_archivo_agenda = 'modelos\\agenda_medicos.csv'

#----------------------------------------------------------------------------------------------
# Inicializa la agenda de médicos con horarios predeterminados
def inicializar_agenda_medicos():
    global agenda
    
    if os.path.exists(ruta_archivo_agenda):
        print("Archivo Agenda existente, inicializando..")
        agenda = cargar_agenda_desde_archivo()
    else:
        print("Creando archivo e Inicializando agenda..")
        medicos = obtener_medicos()   
        # Para cada médico, crea horarios predeterminados de lunes a domingo
        for medico in medicos:
            id_medico = medico["id"]
            for i in range(0, 7): 
                if medico["habilitado"]:
                    hora_inicio = "08:00"
                    hora_fin = "17:00"
                    fecha_actualizacion = datetime.now().strftime("%d-%m-%Y")
                    agenda.append({
                        "id_medico": id_medico,
                        "dia_numero": i,
                        "hora_inicio": hora_inicio,
                        "hora_fin": hora_fin,
                        "fecha_actualizacion": fecha_actualizacion
                    })

    # Guarda la agenda en el archivo agenda_medicos.csv
    guardar_agenda_en_archivo(agenda)
  
#-----------------------------------------------------------------------------------------------  
# Carga la agenda de médicos desde un archivo CSV
def cargar_agenda_desde_archivo():
    try:
        with open(ruta_archivo_agenda, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            agenda = []
            for horario in reader:
                horario['id_medico'] = int(horario['id_medico'])
                horario['dia_numero'] = int(horario['dia_numero'])
                agenda.append(horario)
            return agenda
    except Exception as e:
        print(f"Error al abrir el archivo de agenda: {e}")
        return []

#----------------------------------------------------------------------------------------------
# Guarda la agenda en un archivo CSV
def guardar_agenda_en_archivo(agenda):
    try:
        with open(ruta_archivo_agenda, 'w', newline='', encoding='utf-8') as csvfile:
            campo_nombres = ['id_medico', 'dia_numero', 'hora_inicio', 'hora_fin', 'fecha_actualizacion']
            writer = csv.DictWriter(csvfile, fieldnames=campo_nombres)
            writer.writeheader()
            for horario in agenda:
                writer.writerow(horario)
    except Exception as e:
        print(f"Error al abrir el archivo de agenda: {e}")

#----------------------------------------------------------------------------------------------
# Obtiene la agenda completa de médicos
def obtener_agenda_medicos():
    return agenda

#----------------------------------------------------------------------------------------------
# Obtiene la agenda de un médico específico por su ID
def obtener_agenda_medico_por_id(id_medico):
    global agenda_medico
    agenda_medico = []  
    for medico in agenda:
        if medico["id_medico"] == id_medico:
            agenda_medico.append(medico)
    return agenda_medico

#----------------------------------------------------------------------------------------------
# Crea un nuevo horario en la agenda de un médico
def crear_agenda_medico(id_medico, dia_numero, hora_inicio, hora_fin):
    global agenda
    h_inicio = datetime.strptime(hora_inicio,"%H:%M")
    h_fin = datetime.strptime(hora_fin,"%H:%M")
    for medico in agenda:
        if medico["id_medico"] == id_medico and medico["dia_numero"]!= dia_numero:
                if h_inicio < h_fin:
                    nuevo_horario = {
                        "id_medico": id_medico,
                        "dia_numero": dia_numero,
                        "hora_inicio": hora_inicio,
                        "hora_fin": hora_fin,
                        "fecha_actualizacion": datetime.now().strftime("%d-%m-%Y")
                    }
                    agenda.append(nuevo_horario)
                    guardar_agenda_en_archivo(agenda)
                    return nuevo_horario
                else:
                    return {"error": "La hora de inicio debe ser menor a la hora de fin"}        
        else:
                return {"error": "El día indicado ya está agendado"}
        
#----------------------------------------------------------------------------------------------
# Elimina un día específico de la agenda de un médico por su ID
def eliminar_dia_agenda_medico_por_id(id_medico, dia_numero):
    global agenda
    agenda = [medico for medico in agenda if not (medico["id_medico"] == id_medico and medico["dia_numero"] == dia_numero)]

    try:
        guardar_agenda_en_archivo(agenda)
        return True
    except Exception as e:
        print(f"Error al guardar la agenda en el archivo: {str(e)}")
        return False

#----------------------------------------------------------------------------------------------
# Actualiza un horario específico en la agenda de un médico por su ID y día
def actualizar_agenda_por_dia(id_medico, dia_numero, hora_inicio, hora_fin):
    global agenda
    h_inicio = datetime.strptime(hora_inicio,"%H:%M")
    h_fin = datetime.strptime(hora_fin,"%H:%M")
    for medico in agenda:
        if medico["id_medico"] == id_medico and medico["dia_numero"] == dia_numero:
            if h_inicio < h_fin:
                medico["hora_inicio"] = hora_inicio
                medico["hora_fin"] = hora_fin
                medico["fecha_actualizacion"] = datetime.now().strftime("%d-%m-%Y")
            else:
                return {"error": "La hora de inicio debe ser menor a la de fin"}
            
    guardar_agenda_en_archivo(agenda)
    return agenda
#----------------------------------------------------------------------------------------------
# Obtiene información sobre un día específico en la agenda de un médico por su ID y día
def obtener_dia_agenda(id_medico, fecha_turno):
    fecha_t = datetime.strptime(fecha_turno, "%d-%m-%Y").date()
    dia_turno = fecha_t.strftime('%w')
    # Buscar el día en la agenda del médico
    for medico in agenda:
        if medico["id_medico"] == id_medico and medico["dia_numero"] == int(dia_turno):
            return medico
    
    return None

#----------------------------------------------------------------------------------------------
# Obtiene información sobre un horario específico en la agenda de un médico por su ID y hora
def obtener_hora_agenda(id_medico, hora_turno):
    for medico in agenda:
        if medico["id_medico"] == id_medico and medico["hora_inicio"] < hora_turno < medico["hora_fin"]:
            return medico
    return None

#----------------------------------------------------------------------------------------------
# Obtiene la agenda de un médico por su ID ordenada por día y hora de inicio
def obtener_agenda_ordenada_medicos():
    global agenda
    agenda_ordenada = sorted(agenda, key=lambda medico: (medico["id_medico"], medico["dia_numero"]))
    return agenda_ordenada