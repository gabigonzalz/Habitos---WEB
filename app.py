from flask import render_template, request, redirect, url_for,session
from conexion import app, db
from models import Usuarios,HabitosUsuarios,HabitosPersonalizados,HabitosCompletados
import datetime as dt

#RUTA; SALUDO
@app.route('/')
def index():
    return render_template("index.html")
    

#RUTA; REGISTRO Función que se ejecuta cuando se accede a la URL /registrar.
@app.route("/registrar",methods = ['POST','GET'])
def registrar():
    if request.method == 'POST':
        # Aquí se procesan los datos de registro
        nombre = request.form['nombre']
        contrasena = request.form['contrasena']
        correo = request.form['correo']

        datos_usuario = Usuarios(nombre=nombre, contrasena=contrasena, correo=correo)

        db.session.add(datos_usuario)
        db.session.commit() # metodo parac confirmar todas las operaciones registradas en la sesion
        
        session["id_usuario"] = datos_usuario.id_usuario

        # Después de registrarlo, redirigimos al usuario a la página de inicio de sesión
        return redirect(url_for('iniciar_sesion'))
    return render_template('registrar.html')


#RUTA; INICIO DE SESION 
@app.route('/iniciar_sesion',methods = ['POST','GET'])
def iniciar_sesion():
    if request.method == 'POST':

        contrasena = request.form['contrasena']
        correo = request.form['correo']
        # Buscar el usuario en la base de datos
        datos_usuario = Usuarios.query.filter_by(correo=correo, contrasena=contrasena).first()

        if datos_usuario:
            session["id_usuario"] = datos_usuario.id_usuario
            return redirect(url_for('pagina_principal'))
        else:
            # Manejar error de autenticación
            error = "Correo o contraseña incorrectos"
            return render_template('iniciar_sesion.html', error=error)

    return render_template('iniciar_sesion.html')  # Renderizar el formulario de inicio de sesión


#RUTA; PAGINA PRINCIPAL (HABITOS)
@app.route('/pagina_principal')
def pagina_principal():
    id_usuario = session.get("id_usuario")

    #HabitosUsuarios
    #HabitosPersonalizados


    return render_template('pagina_principal.html')


#RUTA; HISTORIA; (HABITOS)
@app.route('/historial')
def historial_habitos():

#HabitosCompletados

    return render_template("historial.html")


#Siempre al final:
if __name__ == "__main__":
    app.run(debug= True)
