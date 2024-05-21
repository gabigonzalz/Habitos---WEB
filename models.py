from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() #db se convierte en un objeto que nos permite interactuar con la base de datos

#class Usuarios(db.Model): #db.Model indica que Usuarios es un model de datos gestionado por SQLAlchemy
    #id = db.Column(db.Integer, primary_key=True) #Creamos una columna de identificacion para conectar informacion mas adeltante
    #nombre = db.Column(db.String, nullable=False) #Ingrreso de nombre del usuario es decir string y nullable hace para que no se pueda dejar en blanco
    #apellido = db.Column(db.String, nullable=False)
    #cedula = db.Column(db.String, nullable=False)
    #correo = db.Column(db.String,nullable=False)
