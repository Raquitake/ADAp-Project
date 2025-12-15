import os
from datetime import datetime, timezone
from flask import current_app
from werkzeug.utils import secure_filename
from sqlalchemy import func
from models import db, Usuario, Evento, Entrada, Rifa, Boleto, MetaRecaudacion, Donacion
from patterns import AppConfig, PaymentFactory, EventoBuilder, EventTransactionFactory, RaffleTransactionFactory, Subject

class FundraisingFacade(Subject):
    """
    Facade que centraliza la lógica de negocio para:
    - Metas de recaudación
    - Donaciones
    - Gestión de Eventos (y compra de entradas)
    - Gestión de Rifas (y compra de boletos)
    - Validación de QRs
    """

    def __init__(self):
        super().__init__()

    # --- METAS DE RECAUDACIÓN ---

    def get_active_meta(self):
        return MetaRecaudacion.query.filter_by(activa=True).order_by(MetaRecaudacion.fecha_fin.desc()).first()

    def get_all_metas_with_progress(self):
        metas = MetaRecaudacion.query.all()
        datos = []
        for m in metas:
            rec, porc = self.calculate_progress(m)
            datos.append({'obj': m, 'recaudado': rec, 'porcentaje': porc})
        return datos

    def get_meta_by_id(self, meta_id):
        return MetaRecaudacion.query.get_or_404(meta_id)

    def calculate_progress(self, meta):
        if not meta:
            return 0, 0

        inicio = meta.fecha_inicio
        fin = meta.fecha_fin

        # 1. Sumar Entradas vendidas
        total_entradas = db.session.query(func.sum(Entrada.precio)).filter(
            Entrada.fecha_compra >= inicio,
            Entrada.fecha_compra <= fin
        ).scalar() or 0.0

        # 2. Sumar Boletos de Rifa vendidos
        total_boletos = db.session.query(func.sum(Boleto.precio)).filter(
            Boleto.fecha_compra >= inicio,
            Boleto.fecha_compra <= fin
        ).scalar() or 0.0

        # 3. Sumar Donaciones directas
        total_donaciones = db.session.query(func.sum(Donacion.cantidad)).filter(
            Donacion.fecha >= inicio,
            Donacion.fecha <= fin
        ).scalar() or 0.0

        recaudado = total_entradas + total_boletos + total_donaciones
        
        if meta.cantidad_objetivo > 0:
            porcentaje = (recaudado / meta.cantidad_objetivo) * 100
        else:
            porcentaje = 0

        return round(recaudado, 2), min(round(porcentaje, 1), 100)

    def create_meta(self, data, imagen_file):
        try:
            nueva_meta = MetaRecaudacion(
                titulo=data.get('titulo'),
                descripcion=data.get('descripcion'),
                cantidad_objetivo=float(data.get('objetivo', 0)),
                fecha_inicio=datetime.strptime(data.get('fecha_inicio'), '%Y-%m-%dT%H:%M'),
                fecha_fin=datetime.strptime(data.get('fecha_fin'), '%Y-%m-%dT%H:%M'),
                activa=True if data.get('activa') else False
            )

            if imagen_file and imagen_file.filename != '':
                filename = secure_filename(imagen_file.filename)
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                save_name = f"meta_{timestamp}_{filename}"
                
                config = AppConfig()
                upload_dir = os.path.join(current_app.root_path, 'static', 'img', 'metas')
                if not os.path.exists(upload_dir):
                    os.makedirs(upload_dir)
                
                imagen_file.save(os.path.join(upload_dir, save_name))
                nueva_meta.imagen = f"img/metas/{save_name}"

            db.session.add(nueva_meta)
            db.session.commit()
            return True, "Meta creada exitosamente"
        except Exception as e:
            return False, str(e)

    def update_meta(self, meta_id, data, imagen_file):
        try:
            meta = self.get_meta_by_id(meta_id)
            meta.titulo = data.get('titulo')
            meta.descripcion = data.get('descripcion')
            meta.cantidad_objetivo = float(data.get('objetivo', 0))
            meta.activa = True if data.get('activa') else False
            
            f_inicio = data.get('fecha_inicio')
            if f_inicio: meta.fecha_inicio = datetime.strptime(f_inicio, '%Y-%m-%dT%H:%M')
            
            f_fin = data.get('fecha_fin')
            if f_fin: meta.fecha_fin = datetime.strptime(f_fin, '%Y-%m-%dT%H:%M')

            if imagen_file and imagen_file.filename != '':
                if meta.imagen:
                    ruta_antigua = os.path.join(current_app.root_path, 'static', meta.imagen)
                    if os.path.exists(ruta_antigua):
                        try: os.remove(ruta_antigua)
                        except: pass
                
                filename = secure_filename(imagen_file.filename)
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                save_name = f"meta_{timestamp}_{filename}"
                upload_dir = os.path.join(current_app.root_path, 'static', 'img', 'metas')
                if not os.path.exists(upload_dir): os.makedirs(upload_dir)
                    
                imagen_file.save(os.path.join(upload_dir, save_name))
                meta.imagen = f"img/metas/{save_name}"

            db.session.commit()
            return True, "Meta actualizada"
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    def delete_meta(self, meta_id):
        try:
            meta = self.get_meta_by_id(meta_id)
            if meta.imagen:
                ruta_imagen = os.path.join(current_app.root_path, 'static', meta.imagen)
                if os.path.exists(ruta_imagen):
                    try: os.remove(ruta_imagen)
                    except: pass
            
            db.session.delete(meta)
            db.session.commit()
            return True, "Meta eliminada"
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    # --- DONACIONES ---

    def process_donation(self, amount, method, form_data, user_id=None):
        processor = PaymentFactory.get_processor(method)
        if not processor:
            return False, "Método de pago no válido"
        
        success, msg = processor.process(amount, form_data)
        if success:
            try:
                nueva_donacion = Donacion(
                    cantidad=amount,
                    id_usuario=user_id,
                    fecha=datetime.now(timezone.utc)
                )
                db.session.add(nueva_donacion)
                db.session.commit()
                
                # Notificar Observers
                detalles_usuario = {}
                if user_id:
                     u = Usuario.query.get(user_id)
                     if u: detalles_usuario['user_email'] = u.correo_electronico

                self.notify('DONATION_RECEIVED', {
                    'amount': amount, 
                    'user_id': user_id,
                    **detalles_usuario
                })
                
                return True, msg
            except Exception as e:
                db.session.rollback()
                return False, f"Error DB: {str(e)}"
        return False, msg

    # --- EVENTOS ---

    def create_event(self, data, imagen_file):
        try:
            builder = EventoBuilder()
            nuevo_evento = (builder
                .set_basic_info(
                    nombre=data.get('nombre'),
                    localizacion=data.get('localizacion'),
                    informacion=data.get('informacion')
                )
                .set_date(data.get('fecha'))
                .set_price(data.get('precio'))
                .set_image(imagen_file)
                .build()
            )
            db.session.add(nuevo_evento)
            db.session.commit()
            return True, "Evento creado exitosamente"
        except Exception as e:
            return False, str(e)

    def update_event(self, event_id, data, imagen_file):
        try:
            evento = Evento.query.get_or_404(event_id)
            evento.nombre_evento = data.get('nombre')
            evento.localizacion = data.get('localizacion')
            evento.informacion = data.get('informacion')
            
            try: evento.precio = float(data.get('precio', 0.0))
            except: pass
            
            fecha_str = data.get('fecha')
            if fecha_str:
                try: evento.fecha = datetime.strptime(fecha_str, '%Y-%m-%dT%H:%M')
                except: pass
            
            if imagen_file and imagen_file.filename != '':
                config = AppConfig()
                filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{secure_filename(imagen_file.filename)}"
                imagen_file.save(os.path.join(config.get_upload_folder, filename))
                evento.imagen_evento = f"img/eventos/{filename}"

            db.session.commit()
            return True, "Evento actualizado"
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    def delete_event(self, event_id):
        try:
            evento = Evento.query.get_or_404(event_id)
            
            # Borrar imagen
            if evento.imagen_evento:
                titulo = os.path.basename(evento.imagen_evento)
                config = AppConfig()
                path = os.path.join(config.get_upload_folder, titulo)
                if os.path.exists(path):
                    try: os.remove(path)
                    except: pass
            
            # Borrar QRs y Entradas
            entradas = Entrada.query.filter_by(id_evento=evento.id).all()
            for entrada in entradas:
                if entrada.codigo_qr:
                    ruta_qr = os.path.join(current_app.root_path, 'static', entrada.codigo_qr)
                    if os.path.exists(ruta_qr):
                        try: os.remove(ruta_qr)
                        except: pass
            
            Entrada.query.filter_by(id_evento=evento.id).delete()
            db.session.delete(evento)
            db.session.commit()
            return True, "Evento eliminado"
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    def purchase_ticket(self, event_id, quantity, method, form_data, user_id):
        evento = Evento.query.get_or_404(event_id)
        
        processor = PaymentFactory.get_processor(method)
        if not processor:
             return False, "Método de pago desconocido"
             
        total_amount = evento.precio * quantity
        success, msg = processor.process(total_amount, form_data)
        
        if not success:
            return False, msg
            
        # Abstract Factory
        factory = EventTransactionFactory()
        try:
            for _ in range(quantity):
                token_path = factory.create_access_token()
                entrada = factory.create_database_record(evento.id, user_id, evento.precio, token_path)
                db.session.add(entrada)
            db.session.commit()
            
            # Notificar Observers
            detalles = {'event_name': evento.nombre_evento}
            u = Usuario.query.get(user_id)
            if u: detalles['user_email'] = u.correo_electronico
            
            self.notify('TICKET_PURCHASED', detalles)
            
            return True, "Entradas generadas"
        except Exception as e:
            db.session.rollback()
            return False, f"Error generando entradas: {e}"

    def clone_event(self, event_id):
        try:
            original = Evento.query.get_or_404(event_id)
            clon = original.clone()
            db.session.add(clon)
            db.session.commit()
            return True, f"Evento clonado: {clon.nombre_evento}"
        except Exception as e:
            return False, str(e)

    # --- RIFAS ---

    def create_raffle(self, data, imagen_file):
        try:
            precio = 5.0
            try: precio = float(data.get('precio', 5.0))
            except: pass
            
            fecha_fin = None
            f_str = data.get('fecha')
            if f_str:
                try: fecha_fin = datetime.strptime(f_str, '%Y-%m-%dT%H:%M')
                except: pass

            imagen_path = None
            if imagen_file and imagen_file.filename != '':
                config = AppConfig()
                filename = f"rifa_{datetime.now().strftime('%Y%m%d%H%M%S')}_{secure_filename(imagen_file.filename)}"
                imagen_file.save(os.path.join(config.get_rifa_upload_folder, filename))
                imagen_path = f"img/rifas/{filename}"

            nueva_rifa = Rifa(
                nombre=data.get('nombre'),
                premio=data.get('premio'),
                informacion=data.get('informacion'),
                fecha_fin=fecha_fin,
                imagen=imagen_path,
                precio=precio
            )
            db.session.add(nueva_rifa)
            db.session.commit()
            return True, "Rifa creada"
        except Exception as e:
            return False, str(e)

    def update_raffle(self, raffle_id, data, imagen_file):
        try:
            rifa = Rifa.query.get_or_404(raffle_id)
            rifa.nombre = data.get('nombre')
            rifa.premio = data.get('premio')
            rifa.informacion = data.get('informacion')
            
            try: rifa.precio = float(data.get('precio', 5.0))
            except: pass
            
            f_str = data.get('fecha')
            if f_str:
                try: rifa.fecha_fin = datetime.strptime(f_str, '%Y-%m-%dT%H:%M')
                except: pass
                
            if imagen_file:
                pass 

            db.session.commit()
            return True, "Rifa actualizada"
        except Exception as e:
            return False, str(e)

    def delete_raffle(self, raffle_id):
        try:
            rifa = Rifa.query.get_or_404(raffle_id)
            if rifa.imagen:
                config = AppConfig() # Singleton
                filename = os.path.basename(rifa.imagen)
                path = os.path.join(config.get_rifa_upload_folder, filename)
                if os.path.exists(path):
                    try: os.remove(path)
                    except: pass
            
            Boleto.query.filter_by(id_rifa=rifa.id).delete()
            db.session.delete(rifa)
            db.session.commit()
            return True, "Rifa eliminada"
        except Exception as e:
             db.session.rollback()
             return False, str(e)

    def purchase_raffle_tickets(self, raffle_id, quantity, method, form_data, user_id):
        rifa = Rifa.query.get_or_404(raffle_id)
        
        processor = PaymentFactory.get_processor(method)
        if not processor:
             return False, "Método de pago no válido"

        precio_boleto = rifa.precio if rifa.precio else 5.0
        total = precio_boleto * quantity
        
        success, msg = processor.process(total, form_data)
        if not success:
            return False, f"Pago fallido: {msg}"
            
        factory = RaffleTransactionFactory()
        try:
            for _ in range(quantity):
                token = factory.create_access_token()
                record = factory.create_database_record(rifa.id, user_id, precio_boleto, token)
                db.session.add(record)
            db.session.commit()
            
            # Notificar Observers
            detalles = {'raffle_name': rifa.nombre}
            u = Usuario.query.get(user_id)
            if u: detalles['user_email'] = u.correo_electronico
            self.notify('RAFFLE_TICKET_PURCHASED', detalles)

            return True, f"Boletos comprados. {msg}"
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    # --- QR API ---

    def validate_qr(self, content):
        if not content or not content.startswith('TICKET:'):
            return False, 'Formato inválido', None

        try:
            uuid_part = content.split(':', 1)[1]
            # Reconstruir filename esperado
            entrance = Entrada.query.filter_by(codigo_qr=f"img/qrcodes/qr_{uuid_part}.png").first()
            
            if entrance:
                return True, 'Válida', {
                    'evento': entrance.evento.nombre_evento,
                    'asistente': Usuario.query.get(entrance.id_comprador).nombre_usuario,
                    'precio': entrance.precio
                }
            else:
                return False, 'No encontrada', None
        except:
             return False, 'Error procesando', None
