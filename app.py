from flask import render_template, request, redirect, url_for,session
from conexion import app, db
from models import Usuarios,HabitosPersonalizados,HabitosCompletados, HabitosUsuarios
import datetime as dt

# RUTAS Y FUNCIONES DEL PROGRAMA #

#RUTA; SALUDO AL USUARIO
@app.route('/')
def index():
    return render_template("index.html")
    


#RUTA; REGISTRO
@app.route("/registrar",methods = ['POST','GET'])
def registrar():
    if request.method == 'POST':
        # Aquí se guardan los datos
        nombre = request.form['nombre']
        contrasena = request.form['contrasena']
        correo = request.form['correo']

        # Los metemos en la base
        datos_usuario = Usuarios(nombre=nombre, contrasena=contrasena, correo=correo)

        db.session.add(datos_usuario)
        db.session.commit()

        # Definimos la sesion especifica para el usuario
        session["id_usuario"] = datos_usuario.id_usuario

        # Redirigimos al usuario a la página de inicio de sesión
        return redirect(url_for('iniciar_sesion'))
    return render_template('registrar.html')



#RUTA; INICIO DE SESION 
@app.route('/iniciar_sesion',methods = ['POST','GET'])
def iniciar_sesion():
    if request.method == 'POST':

        # Pedimos al usuario su contrasena y su correo
        contrasena = request.form['contrasena']
        correo = request.form['correo']

        # Buscar el usuario en la base
        datos_usuario = Usuarios.query.filter_by(correo=correo, contrasena=contrasena).first()

        # Si lo encuentra le mostramos su pagina principal
        if datos_usuario:
            session["id_usuario"] = datos_usuario.id_usuario
            return redirect(url_for('pagina_principal'))
        else:
            # Si es que falla el usuario
            error = "Correo o contraseña incorrectos"
            return render_template('iniciar_sesion.html', error=error)

    return render_template('iniciar_sesion.html')



#RUTA; PARA ANHADIR UN HABITO NUEVO
@app.route('/agregar_habito', methods=['POST', 'GET'])
def agregar_habito():
    if request.method == 'POST':
        # Pedimos el habito al usuario en especifico (especificado por su ID)
        nuevo_habito = request.form.get("nuevo_habito_input")
        id_usuario = session.get("id_usuario")

        # SI se agrega un nuevo habito lo cargamos a sus habitos personalizados
        if id_usuario and nuevo_habito:
            nuevo_habito_personalizado = HabitosPersonalizados(habito_nombre=nuevo_habito, id_usuario=id_usuario)
            db.session.add(nuevo_habito_personalizado)
            db.session.commit()

            # Volvemos a la pagina principal o damos error
            return redirect(url_for('pagina_principal'))
        else:
            return redirect(url_for('pagina_principal', error="Error al agregar el hábito nuevo"))

    return render_template('agregar_habito.html')



#RUTA; PAGINA PRINCIPAL (HABITOS)
@app.route('/pagina_principal')
def pagina_principal():
    # Especificamos la sesion
    id_usuario = session.get("id_usuario")

    # Si no encontramos el usuario entonces volvemos a inicio de sesion
    if not id_usuario:
        return redirect(url_for('iniciar_sesion'))

    # Definimos el usuario y sus habitos personalizados a mostrar
    usuario = Usuarios.query.get(id_usuario)
    habitos_personalizados = HabitosPersonalizados.query.filter_by(id_usuario=id_usuario).all()

    return render_template('pagina_principal.html', usuario=usuario, habitos_personalizados=habitos_personalizados)



#RUTA; HISTORIA; (HABITOS)
@app.route('/historial')
def historial_habitos():

# Aqui iria el historial de los habitos completados
# A realizar

    return render_template("historial.html")





# Siempre al final para poder ejecutar el programa
if __name__ == "__main__":
    app.run(debug= True)
