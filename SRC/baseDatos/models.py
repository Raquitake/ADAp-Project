from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

# --- TABLAS INTERMEDIAS (Gestión) ---

class GestionaRifa(db.Model):
    __tablename__ = 'gestiona_rifa'
    id_administrador = db.Column(db.Integer, db.ForeignKey('administrador.id'), primary_key=True)
    id_rifa = db.Column(db.Integer, db.ForeignKey('rifa.id'), primary_key=True)
    admin_role = db.Column(db.String(50)) 

class GestionaEvento(db.Model):
    __tablename__ = 'gestiona_evento'
    id_administrador = db.Column(db.Integer, db.ForeignKey('administrador.id'), primary_key=True)
    id_evento = db.Column(db.Integer, db.ForeignKey('evento.id'), primary_key=True)
    admin_role = db.Column(db.String(50))

class GestionaVoluntario(db.Model):
    __tablename__ = 'gestiona_voluntario'
    id = db.Column(db.Integer, primary_key=True)
    id_voluntario = db.Column(db.Integer, db.ForeignKey('voluntario.id'))
    id_administrador = db.Column(db.Integer, db.ForeignKey('administrador.id'))
    id_evento = db.Column(db.Integer, db.ForeignKey('evento.id'))

# --- USUARIOS Y ROLES ---

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(100), nullable=False)
    correo_electronico = db.Column(db.String(120), unique=True, nullable=False)
    contrasena_hash = db.Column(db.String(200), nullable=False)
    dni_nif = db.Column(db.String(20), unique=True, nullable=True) 
    es_socio = db.Column(db.Boolean, default=False)

    # Relaciones de Roles
    admin_perfil = db.relationship('Administrador', backref='usuario', uselist=False)
    voluntario_perfil = db.relationship('Voluntario', backref='usuario', uselist=False)

    # Propiedades de ayuda
    @property
    def es_admin(self):
        return self.admin_perfil is not None

class Administrador(db.Model):
    __tablename__ = 'administrador'
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), unique=True)
    # admin_role puede gestionarse aquí o en las tablas de relación dependiendo de la granularidad

class Voluntario(db.Model):
    __tablename__ = 'voluntario'
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), unique=True, nullable=False)

# --- MENSAJERÍA ---

class Mensaje(db.Model):
    __tablename__ = 'mensaje'
    id = db.Column(db.Integer, primary_key=True)
    contenido = db.Column(db.Text)
    emisor = db.Column(db.String(100)) 
    id_certificado_contenido = db.Column(db.Integer, db.ForeignKey('certificado.id'), nullable=True)
    id_recibo_contenido = db.Column(db.Integer, db.ForeignKey('recibo.id'), nullable=True)

class Destinatarios(db.Model):
    __tablename__ = 'destinatarios'
    id = db.Column(db.Integer, primary_key=True)
    id_mensaje = db.Column(db.Integer, db.ForeignKey('mensaje.id'))
    id_destinatario = db.Column(db.Integer, db.ForeignKey('usuario.id')) 

# --- EVENTOS Y RIFAS ---

class Evento(db.Model):
    __tablename__ = 'evento'
    id = db.Column(db.Integer, primary_key=True)
    nombre_evento = db.Column(db.String(150))
    localizacion = db.Column(db.String(200))
    fecha = db.Column(db.DateTime)
    informacion = db.Column(db.Text)

class Rifa(db.Model):
    __tablename__ = 'rifa'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150))
    fecha_fin = db.Column(db.DateTime)
    informacion = db.Column(db.Text)
    ganador_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=True) 

# --- TRANSACCIONES (ENTRADAS Y BOLETOS) ---

class Entrada(db.Model):
    __tablename__ = 'entrada'
    
    id = db.Column(db.Integer, primary_key=True)
    precio = db.Column(db.Float)
    asiento = db.Column(db.String(50))
    enlace_evento = db.Column(db.String(255))
    codigo_qr = db.Column(db.String(255))
    
    # Claves foráneas
    id_evento = db.Column(db.Integer, db.ForeignKey('evento.id'))
    id_comprador = db.Column(db.Integer, db.ForeignKey('usuario.id')) 

class Boleto(db.Model):
    __tablename__ = 'boleto'
    
    id = db.Column(db.Integer, primary_key=True)
    precio = db.Column(db.Float)
    
    # Claves foráneas
    id_rifa = db.Column(db.Integer, db.ForeignKey('rifa.id'))
    id_comprador = db.Column(db.Integer, db.ForeignKey('usuario.id')) 

class Recibo(db.Model):
    __tablename__ = 'recibo'
   
    id = db.Column(db.Integer, primary_key=True)
    importe = db.Column(db.Float)
    tipo_de_origen = db.Column(db.String(50)) 
    id_origen = db.Column(db.Integer) 
    
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    id_mensaje = db.Column(db.Integer, db.ForeignKey('mensaje.id'), nullable=True)

class Certificado(db.Model):
    __tablename__ = 'certificado'
    
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    id_recibo_emision = db.Column(db.Integer, db.ForeignKey('recibo.id'))
    id_mensaje = db.Column(db.Integer, db.ForeignKey('mensaje.id'), nullable=True)