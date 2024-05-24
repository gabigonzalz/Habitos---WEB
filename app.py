# Importamos las funciones necesarias
from flask import render_template, request, redirect, url_for,session
from conexion import app, db
from models import Usuarios,HabitosPersonalizados,HabitosCompletados, HabitosUsuarios
from datetime import datetime

##### RUTAS Y FUNCIONES DEL PROGRAMA #####

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



# RUTA; PARA REGISTRAR UN HÁBITO COMPLETADO
@app.route('/completar_habito/<int:id_habito>', methods=['POST'])  
def completar_habito(id_habito):
    if session.get("id_usuario"):  # Verifica el usuario

        # Crea un nuevo registro del hábito completado
        nuevo_habito_completado = HabitosCompletados(
            id_usuario=session["id_usuario"],  # ID del usuario autenticado
            id_habito_personalizado=id_habito,  # ID del hábito que se está completando
            fecha_completado=datetime.today()  # Marca de tiempo de cuando se completó el hábito
            )
        
        db.session.add(nuevo_habito_completado)
        db.session.commit()
    # Volvemos a la pagina
    return redirect(url_for('pagina_principal'))



#RUTA; FUNCION ELIMINAR HABITO
@app.route('/eliminar_habito/<int:id_habito>', methods=['POST'])
def eliminar_habito(id_habito):
    id_usuario = session.get("id_usuario") # Obtener el ID
    
    if id_usuario:
        habito_a_eliminar = HabitosPersonalizados.query.filter_by(id_habitos_personalizados=id_habito, id_usuario=id_usuario).first()
        
        if habito_a_eliminar: # Si se encuentra el hábito a eliminar
            db.session.delete(habito_a_eliminar) # Eliminar el hábito de la base de datos

            db.session.commit()

            return redirect(url_for('pagina_principal'))
        
    # Si no se encuentra el hábito o no hay un usuario en sesión, redirigir a la página principal
    return redirect(url_for('pagina_principal', error="Error al eliminar el hábito"))



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



# RUTA; HISTORIAL DE HÁBITOS COMPLETADOS
@app.route('/historial') 
def historial_habitos():
    id_usuario = session.get("id_usuario") # Obtener el ID 

    if not id_usuario: # Si no hay un usuario en sesión, redirigir a la página de inicio de sesión
        return redirect(url_for('iniciar_sesion'))

    usuario = Usuarios.query.get(id_usuario) # Obtener los datos del usuario

    # Obtener los hábitos completados por el usuario
    habitos_completados = db.session.query(HabitosCompletados, HabitosPersonalizados)\
                        .join(HabitosPersonalizados, HabitosCompletados.id_habito_personalizado == HabitosPersonalizados.id_habitos_personalizados)\
                        .filter(HabitosCompletados.id_usuario == id_usuario).all()

    return render_template("historial.html", usuario=usuario, habitos_completados=habitos_completados)



#RUTA; LIMPIAR EL HISTORIAL DEL USUARIO
@app.route('/borrar_todo_historial', methods=['POST'])
def borrar_todo_historial():

    id_usuario = session.get("id_usuario")
    # Filtramos todos los habitos completados del usuario
    if id_usuario:
        habitos_completados = HabitosCompletados.query.filter_by(id_usuario=id_usuario).all()
        # Iteramos cada uno de los habitos para eliminar
        for habito_completado in habitos_completados:
            db.session.delete(habito_completado)

        db.session.commit()
    # Mostramos el historial limpio
    return redirect(url_for('historial_habitos'))



#RUTA; BORRAR UN HABITO COMPLETADO EN ESPECIFICO
@app.route('/borrar_habito/<int:id_habito_completado>', methods=['POST'])
def borrar_habito(id_habito_completado):

    id_usuario = session.get("id_usuario")
    # Filtramos todos los habitos completados del usuario
    if id_usuario:
        # Busca el habito completado por el id del usario y el id habito coompletado
        habito_completado = HabitosCompletados.query.filter_by(id_usuario=id_usuario, id_habitos_completados=id_habito_completado).first()
        
        # Si se encuentra el habito
        if habito_completado:
            db.session.delete(habito_completado)

            db.session.commit()

    return redirect(url_for('historial_habitos'))



# Siempre al final para poder ejecutar el programa
if __name__ == "__main__":
    app.run(debug= True)
