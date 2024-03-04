# -----------------------------------------------------------------
# Módulo de funciones sobre Pacientes
# -----------------------------------------------------------------

import requests
import csv
import os

# Variables globales que usaremos en este módulo
pacientes = []
id_paciente = 0  # Variable para asignar IDs únicos a los usuarios
ruta_archivo_pacientes = 'modelos\\pacientes.csv'

#----------------------------------------------------------------------------------------------

# Inicializa la lista de pacientes, cargándola desde un archivo CSV o una API si es necesario
def inicializar_pacientes():
    global id_paciente
    archivo_csv = 'pacientes.csv'

    try:
        # Verifica si el archivo CSV ya existe
        if os.path.exists(ruta_archivo_pacientes):
            print("El archivo pacientes.csv ya existe. Cargando datos desde el archivo...")
            importar_datos_pacientes_desde_csv()
        else:
            print("El archivo pacientes.csv no existe. Cargando datos desde API...")
            url = 'https://randomuser.me/api/?results=50&inc=id,name,login,phone,email,location,password,nat,value&password=number,6&nat=es&value=number,8&phone=number,10'

            response_pacientes = requests.get(url, verify=False)

            codigo_respuesta = response_pacientes.status_code

            if codigo_respuesta == 200:
                respuesta = response_pacientes.json()
                # Crear el archivo CSV
                crear_archivo_pacientes(respuesta)
                # Cargar datos desde el archivo CSV
                importar_datos_pacientes_desde_csv()
            else:
                print(f"Error al obtener datos desde la API. Código de respuesta: {codigo_respuesta}")
                # Devuelve un diccionario con información sobre el error
                return {"error": f"Error al obtener datos desde la API. Código de respuesta: {codigo_respuesta}"}

    except requests.exceptions.SSLError as e:
        print(f"Error de conexión SSL: {e}")
        # Devuelve un diccionario con información sobre el error
        return {"error": f"Error de conexión SSL: {e}"}

    # Devuelve un diccionario con información sobre el éxito de la operación
    return {"correcto": "Datos de pacientes cargados correctamente"}

    
#----------------------------------------------------------------------------------------------

# Crea un archivo CSV con datos de pacientes obtenidos de una respuesta API
def crear_archivo_pacientes(respuesta):
    global id_paciente
    try:
        with open(ruta_archivo_pacientes, 'w', newline='', encoding='utf-8') as csvfile:
            campo_nombres = ['id', 'dni', 'nombre', 'apellido', 'telefono', 'email', 'dir_calle','dir_numero']
            writer = csv.DictWriter(csvfile, fieldnames=campo_nombres)
            writer.writeheader()
            for paciente in respuesta["results"]:
                id_paciente += 1
                dni = paciente["id"]["value"].replace('-', '').rstrip('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
                nombre = paciente["name"]["first"]
                apellido = paciente["name"]["last"]
                telefono = paciente["phone"].replace('-', '')
                email = paciente["email"]
                dir_calle = paciente.get("location", {}).get("street", {}).get("name", "")
                dir_numero = paciente.get("location", {}).get("street", {}).get("number", "")
       
                # Escribir en el archivo CSV
                writer.writerow({
                    'id': id_paciente,
                    'dni': dni,
                    'nombre': nombre,
                    'apellido': apellido,
                    'telefono': telefono,
                    'email': email,
                    'dir_calle': dir_calle,
                    'dir_numero': dir_numero
                })
    except Exception as e:
        print(f"Error al abrir el archivo: {e}")

#----------------------------------------------------------------------------------------------

# Importa datos de pacientes desde un archivo CSV
def importar_datos_pacientes_desde_csv():
    global pacientes
    global id_paciente
    pacientes = []  # Limpiamos la lista de pacientes antes de importar desde el archivo CSV
    with open(ruta_archivo_pacientes, newline='',encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Convertimos el ID de cadena a entero
            row['id'] = int(row['id'])
            pacientes.append(row) 
    if len(pacientes)>0:
        id_paciente = pacientes[-1]["id"]+1
    else:
        id_paciente = 1

#----------------------------------------------------------------------------------------------

# Exporta la lista de pacientes a un archivo CSV
def exportar_a_csv():
    with open(ruta_archivo_pacientes, 'w', newline='',encoding='utf-8') as csvfile:
        campo_nombres = ['id', 'dni', 'nombre', 'apellido', 'telefono', 'email', 'dir_calle','dir_numero']
        writer = csv.DictWriter(csvfile, fieldnames=campo_nombres)
        writer.writeheader()
        for paciente in pacientes:
            writer.writerow(paciente)

#----------------------------------------------------------------------------------------------

# Obtiene la lista completa de pacientes
def obtener_pacientes():
    return pacientes

#----------------------------------------------------------------------------------------------

# Obtiene un paciente específico por su ID
def obtener_paciente_por_id(id_paciente):
    for paciente in pacientes:
        if paciente["id"] == id_paciente:
            return paciente

    return None

#----------------------------------------------------------------------------------------------

# Crea un nuevo paciente y lo agrega a la lista
def crear_paciente(dni,nombre, apellido, telefono, email,dir_calle,dir_numero):
    global id_paciente
    # Agrega el paciente a la lista con un ID único
    pacientes.append({
        "id": id_paciente,
        "dni": dni,
        "nombre": nombre,
        "apellido": apellido,
        "telefono": telefono,
        "email": email,
        "dir_calle": dir_calle,
        "dir_numero": dir_numero
    })
    id_paciente += 1
    exportar_a_csv()
    return pacientes[-1]

#----------------------------------------------------------------------------------------------

# Actualiza la información de un paciente existente por su ID
def actualizar_paciente_por_id(id_paciente,dni, nombre, apellido, telefono, email,dir_calle,dir_numero):
    for paciente in pacientes:
        if paciente["id"] == id_paciente:
            paciente["dni"] = dni
            paciente["nombre"] = nombre
            paciente["apellido"] = apellido
            paciente["telefono"] = telefono
            paciente["email"] = email
            paciente["dir_calle"] = dir_calle
            paciente["dir_numero"] = dir_numero
            
            exportar_a_csv()
            return paciente
    # Devuelve None si no se encuentra el paciente
    return None

#----------------------------------------------------------------------------------------------

# Elimina un paciente por su ID
def eliminar_paciente_por_id(id_paciente):
    global pacientes
    for paciente in pacientes:
        if paciente["id"] == id_paciente:
            pacientes.remove(paciente)
            exportar_a_csv()  
            return True  
    return False  

#----------------------------------------------------------------------------------------------

# Obtiene un paciente por su DNI
def obtener_paciente_por_dni(dni):
    for paciente in pacientes:
        if paciente["dni"] == dni:
            return paciente
    return None    