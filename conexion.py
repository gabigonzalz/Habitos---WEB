# Importamos las funciones necesarias
from models import db #Para interactuar con los modelos de la base de datos
from flask import Flask

app = Flask(__name__)

#UNA URI UNIFORM RESOURCE IDENTIFIER de base de datos es un acadena de texto que especifica la ubicacion y los detalles de conexion para la base de datos que queremos usar en nuestra aplicacion

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///base_de_datos.db"

app.config["SECRET_KEY"] = "aaabbbcccddd"

db.init_app(app) #inicializa la aplicacion de flask con la configuracion de SQLAlchemy

with app.app_context():
    db.create_all()