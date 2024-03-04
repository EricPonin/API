from flask import Flask
from modelos.medico import inicializar_medicos
from modelos.paciente import inicializar_pacientes
from modelos.agenda_medico import inicializar_agenda_medicos
from modelos.turno import importar_datos_turnos_desde_csv
from controladores.rutas_medicos import medicos_bp
from controladores.rutas_pacientes import pacientes_bp
from controladores.rutas_agenda_medico import agenda_medicos_bp
from controladores.rutas_turnos import turnos_bp

app = Flask(__name__) #creamos una instancia de la clase Flask

inicializar_medicos()
inicializar_pacientes()
inicializar_agenda_medicos()
importar_datos_turnos_desde_csv()

# registramos el blueprint
app.register_blueprint(medicos_bp)
app.register_blueprint(pacientes_bp)
app.register_blueprint(agenda_medicos_bp)
app.register_blueprint(turnos_bp)

if __name__ == '__main__':
    app.run(debug=True) #iniciamos la aplicación