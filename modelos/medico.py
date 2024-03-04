# --------------------------------------------------------------------------------------------
# Módulo de funciones sobre Medicos
# --------------------------------------------------------------------------------------------

import requests
import csv
import os

# Variables globales que usaremos en este módulo
medicos = []
id_medico = 0  # Variable para asignar IDs únicos a los médicos
ruta_archivo_medicos = 'modelos\\medicos.csv'

#----------------------------------------------------------------------------------------------

# Inicializa la lista de médicos, cargándola desde un archivo CSV o una API si es necesario
def inicializar_medicos():
    global id_medico
    archivo_csv = 'medicos.csv'

    try:
        # Verifica si el archivo CSV ya existe
        if os.path.exists(ruta_archivo_medicos):
            print("El archivo medicos.csv ya existe. Cargando datos desde el archivo...")
            importar_datos_medicos_desde_csv()
        else:
            print("El archivo medicos.csv no existe. Cargando datos desde API...")
            url = 'https://randomuser.me/api/?results=10&inc=id,name,login,phone,email,password,nat,value&password=number,6&nat=es&value=number,8&phone=number,10'

            response_medicos = requests.get(url, verify=False)
            
            codigo_respuesta = response_medicos.status_code

            if codigo_respuesta == 200:
                respuesta = response_medicos.json()
                # Crea el archivo CSV
                crear_archivo_medicos(respuesta)
                # Carga datos desde el archivo CSV
                importar_datos_medicos_desde_csv()
            else:
                print(f"Error al obtener datos desde la API. Código de respuesta: {codigo_respuesta}")
                # Devuelve un diccionario con información sobre el error
                return {"error": f"Error al obtener datos desde la API. Código de respuesta: {codigo_respuesta}"}

    except requests.exceptions.SSLError as e:
        print(f"Error de conexión SSL: {e}")
        # Devuelve un diccionario con información sobre el error
        return {"error": f"Error de conexión SSL: {e}"}

    # Devuelve un diccionario con información sobre el éxito de la operación
    return {"correcto": "Datos de médicos cargados correctamente"}


#----------------------------------------------------------------------------------------------

# Crea un archivo CSV con datos de médicos obtenidos de una respuesta API
def crear_archivo_medicos(respuesta):
    global id_medico
    try:
        with open(ruta_archivo_medicos, 'w', newline='', encoding='utf-8') as csvfile:
            campo_nombres = ['id', 'dni', 'nombre', 'apellido', 'matricula', 'telefono', 'email', 'habilitado']
            writer = csv.DictWriter(csvfile, fieldnames=campo_nombres)
            writer.writeheader()
            for medico in respuesta["results"]:
                id_medico += 1
                dni = medico["id"]["value"].replace('-', '').rstrip('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
                nombre = medico["name"]["first"]
                apellido = medico["name"]["last"]
                matricula = medico.get("login", {}).get("password", "")
                telefono = medico["phone"].replace('-', '')
                email = medico["email"]
                habilitado = True 
                # Escribir en el archivo CSV
                writer.writerow({
                    'id': id_medico,
                    'dni': dni,
                    'nombre': nombre,
                    'apellido': apellido,
                    'matricula': matricula,
                    'telefono': telefono,
                    'email': email,
                    'habilitado': habilitado
                })
    except Exception as e:
        print(f"Error al abrir el archivo: {e}")

#----------------------------------------------------------------------------------------------

# Importa datos de médicos desde un archivo CSV
def importar_datos_medicos_desde_csv():
    global medicos
    global id_medico
    medicos = []  # Limpiamos la lista de médicos antes de importar desde el archivo CSV
    with open(ruta_archivo_medicos, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Convertimos el ID de cadena a entero
            row['id'] = int(row['id'])
            row['matricula'] = int(row['matricula'])
            medicos.append(row) 
    if len(medicos)>0:
        id_medico = medicos[-1]["id"]+1
    else:
        id_medico = 1

#----------------------------------------------------------------------------------------------
     
# Exporta la lista de médicos a un archivo CSV
def exportar_a_csv():
    with open(ruta_archivo_medicos, 'w', newline='',encoding='utf-8') as csvfile:
        campo_nombres = ['id', 'dni', 'nombre', 'apellido', 'matricula', 'telefono', 'email', 'habilitado']
        writer = csv.DictWriter(csvfile, fieldnames=campo_nombres)
        writer.writeheader()
        for medico in medicos:
            writer.writerow(medico)

#----------------------------------------------------------------------------------------------
      
# Obtiene la lista completa de médicos
def obtener_medicos():
    return medicos

#----------------------------------------------------------------------------------------------

# Obtiene un médico específico por su ID
def obtener_medico_por_id(id_medico):
    for medico in medicos:
        if medico["id"] == id_medico:
            return medico
    return None

#----------------------------------------------------------------------------------------------

# Crea un nuevo médico y lo agrega a la lista
def crear_medico(dni, nombre, apellido, matricula, telefono, email, habilitado):
    global id_medico
    habilitado = habilitado.lower() == 'true'
    
    medicos.append({
        "id": id_medico,
        "dni": dni,
        "nombre": nombre,
        "apellido": apellido,
        "matricula": matricula,
        "telefono": telefono,
        "email": email,
        "habilitado": habilitado
    })
    id_medico += 1
    exportar_a_csv()
 
    return medicos[-1]

#----------------------------------------------------------------------------------------------

# Actualiza la información de un médico existente por su ID
def actualizar_medico_por_id(id_medico, dni, nombre, apellido, matricula, telefono, email, habilitado):
    for medico in medicos:
        if medico["id"] == id_medico:
            
            medico["dni"] = dni
            medico["nombre"] = nombre
            medico["apellido"] = apellido
            medico["matricula"] = matricula
            medico["telefono"] = telefono
            medico["email"] = email
            medico["habilitado"] = habilitado
            
            exportar_a_csv()
            return medico
   
    return None

#----------------------------------------------------------------------------------------------

# Obtiene un médico habilitado específico por su ID
def obtener_medico_habilitado(id_medico):
    for medico in medicos:
        if medico["id"] == id_medico and medico["habilitado"] == "true":
            return medico
    return None
