from flask_sqlalchemy import SQLAlchemy
import datetime as dt

db = SQLAlchemy()

#Creacion de usuarios
class Usuarios(db.Model):
    id_usuario = db.Column(db.Integer, primary_key=True) 
    nombre = db.Column(db.String, nullable=False) 
    contrasena = db.Column(db.String(6), nullable=False)
    correo = db.Column(db.String, nullable=False)

    def __init__(self, nombre, contrasena, correo):
        self.nombre = nombre
        self.contrasena = contrasena
        self.correo = correo

#Relaciona usuarios con sus hábitos personalizados
class HabitosUsuarios(db.Model):
    id_habitos_usuarios = db.Column(db.Integer, primary_key=True)  #Identificador unico de la relación entre usuario y el habito
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id_usuario"), nullable=False) 
    id_habito_personalizado = db.Column(db.Integer, db.ForeignKey("habitos_personalizados.id_habitos_personalizados"), nullable=True) 

    def __init__(self, id_usuario, id_habito_personalizado):
        self.id_usuario = id_usuario
        self.id_habito_personalizado = id_habito_personalizado

#Hábitos personalizados creados por los usuarios
class HabitosPersonalizados(db.Model):
    id_habitos_personalizados = db.Column(db.Integer, primary_key=True) 
    habito_nombre = db.Column(db.String, nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id_usuario"), nullable=False)

    def __init__(self, habito_nombre, id_usuario):
        self.habito_nombre = habito_nombre
        self.id_usuario = id_usuario

#Hábitos que los usuarios completan
class HabitosCompletados(db.Model):
    id_habitos_completados = db.Column(db.Integer, primary_key=True)  
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id_usuario"), nullable=False)  
    id_habito_personalizado = db.Column(db.Integer, db.ForeignKey("habitos_personalizados.id_habitos_personalizados"), nullable=True) 
    fecha_completado = db.Column(db.String, nullable=False)

    def __init__(self, id_habito_personalizado, id_usuario, fecha_completado):
        self.id_habito_personalizado = id_habito_personalizado
        self.id_usuario = id_usuario
        self.fecha_completado = fecha_completado