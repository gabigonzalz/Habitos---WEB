from flask import render_template, request, redirect, url_for,session
from conexion import app, db
from models import Usuarios

#RUTA; SALUDO
@app.route('/')
def index():
    return render_template("index.html")
    

#RUTA; REGISTRO Función que se ejecuta cuando se accede a la URL /registrar.
@app.route("/registrar",methods = ['POST','GET'])
def registrar():
    if request.method == 'POST':
        # Aquí se procesan los datos de registro
        # Después de registrarlo, redirigimos al usuario a la página de inicio de sesión
        return redirect(url_for('iniciar_sesion.html'))
    return render_template('registrar.html')


#RUTA; INICIO DE SESION 
@app.route('/iniciar_sesion',methods = ['POST','GET'])
def iniciar_sesion():
    if request.method == 'POST':
        #Ingresa datos de nuevo  p/ validar
        nombre = request.form['nombre']
        contrasenha = request.form['contrasenha']
        correo = request.form['correo']

        # Aquí va la lógica para verificar los datos de inicio de sesión
        # Si son válidos, redirigen al usuario a la página principal 
        return redirect(url_for('pagina_principal.html'))

    return render_template('iniciar_sesion.html')  # Renderizar el formulario de inicio de sesión


#RUTA; PAGINA PRINCIPAL (HABITOS)
@app.route('/pagina_principal')
def pagina_principal():
    
    return render_template('pagina_principal.html')


#RUTA; HISTORIA; (HABITOS)
@app.route('/historial')
def historial_habitos():

    return render_template("historial.html")


#Siempre al final:
if __name__ == "__main__":
    app.run(debug= True)
