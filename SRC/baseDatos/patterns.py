import os
import qrcode
import uuid
import re
from datetime import datetime
from abc import ABC, abstractmethod
from werkzeug.utils import secure_filename
from models import Evento, Entrada, Boleto, db
from flask import current_app

# 1. SINGLETON: Configuración de la aplicación

class AppConfig:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AppConfig, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance
    
    def init_app(self, app):
        """Inicializa configuración una sola vez."""
        if not self.initialized:
            self.upload_folder = app.config.get('UPLOAD_FOLDER')
            self.rifa_upload_folder = app.config.get('RIFA_UPLOAD_FOLDER')
            self.qr_upload_folder = app.config.get('QR_UPLOAD_FOLDER')
            
            # Asegurar directorios
            for folder in [self.upload_folder, self.rifa_upload_folder, self.qr_upload_folder]:
                if folder and not os.path.exists(folder):
                    os.makedirs(folder, exist_ok=True)
                    
            self.initialized = True
    
    @property
    def get_upload_folder(self):
        return self.upload_folder
        
    @property
    def get_rifa_upload_folder(self):
        return self.rifa_upload_folder

    @property
    def get_qr_upload_folder(self):
        return self.qr_upload_folder

# 2. FACTORY METHOD: Factory de pagos

class PaymentProcessor(ABC):
    @abstractmethod
    def process(self, amount, form_data):
        pass

class CardProcessor(PaymentProcessor):
    def process(self, amount, form_data):
        numero = form_data.get('tarjeta_numero', '').replace(' ', '')
        cvv = form_data.get('tarjeta_cvv', '').strip()
        
        if not re.match(r'^\d{16}$', numero):
            return False, 'Tarjeta inválida (16 dígitos).'
        if not re.match(r'^\d{3}$', cvv):
            return False, 'CVV inválido.'
        return True, 'Pago con tarjeta simulado exitoso.'

class BizumProcessor(PaymentProcessor):
    def process(self, amount, form_data):
        telefono = form_data.get('telefono', '').strip()
        # Validación simple simulada
        return True, 'Pago Bizum simulado exitoso.'

class PaypalProcessor(PaymentProcessor):
    def process(self, amount, form_data):
        return True, 'Redirección PayPal simulada exitosa.'

class PaymentFactory:
    @staticmethod
    def get_processor(method_name) -> PaymentProcessor:
        processors = {
            'tarjeta': CardProcessor(),
            'bizum': BizumProcessor(),
            'paypal': PaypalProcessor()
        }
        return processors.get(method_name)

# 3. BUILDER: EventoBuilder

class EventoBuilder:
    def __init__(self):
        self.evento = Evento()
    
    def set_basic_info(self, nombre, localizacion, informacion):
        self.evento.nombre_evento = nombre
        self.evento.localizacion = localizacion
        self.evento.informacion = informacion
        return self
        
    def set_date(self, fecha_str):
        if fecha_str:
            try:
                self.evento.fecha = datetime.strptime(fecha_str, '%Y-%m-%dT%H:%M')
            except ValueError:
                self.evento.fecha = None
        return self
        
    def set_price(self, precio):
        try:
            self.evento.precio = float(precio) if precio else 0.0
        except ValueError:
            self.evento.precio = 0.0
        return self
        
    def set_image(self, file_storage):
        if file_storage and file_storage.filename:
            config = AppConfig() # Singleton
            folder = config.get_upload_folder
            
            filename = secure_filename(file_storage.filename)
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            filename = f"{timestamp}_{filename}"
            
            file_storage.save(os.path.join(folder, filename))
            self.evento.imagen_evento = f"img/eventos/{filename}"
        elif not self.evento.imagen_evento:
             # Default o conservar logic podría ir aquí
             pass
        return self
        
    def build(self):
        return self.evento


# 4. ABSTRACT FACTORY: Factory de transacciones

# Familia de objetos: DbRecord (Entrada/Boleto) y AccessToken (QR/Nada)

class TransactionFactory(ABC):
    @abstractmethod
    def create_database_record(self, item_id, user_id, price, extra_data=None):
        pass
        
    @abstractmethod
    def create_access_token(self):
        pass

class EventTransactionFactory(TransactionFactory):
    def create_access_token(self):
        # Generar QR
        config = AppConfig()
        unique_id = str(uuid.uuid4())
        qr_data = f"TICKET:{unique_id}"
        
        qr_img = qrcode.make(qr_data)
        qr_filename = f"qr_{unique_id}.png"
        qr_path_full = os.path.join(config.get_qr_upload_folder, qr_filename)
        qr_img.save(qr_path_full)
        
        return f"img/qrcodes/{qr_filename}"

    def create_database_record(self, item_id, user_id, price, qr_path):
        return Entrada(
            precio=price,
            id_evento=item_id,
            id_comprador=user_id,
            codigo_qr=qr_path
        )

class RaffleTransactionFactory(TransactionFactory):
    def create_access_token(self):
        # Rifas sin QR
        return None

    def create_database_record(self, item_id, user_id, price, token=None):
        return Boleto(
            id_rifa=item_id,
            id_comprador=user_id,
            precio=price
        )
