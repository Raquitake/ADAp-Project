import os
import re

from flask import Flask, render_template, redirect, url_for, request, flash, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
from datetime import datetime
from models import db, Usuario, Administrador, Evento, Entrada, Rifa 

def validar_dni_nie(documento):
    # Limpiamos el input (mayúsculas y sin espacios)
    documento = documento.upper().strip()
    
    # Comprobamos formato básico (longitud 9 caracteres)
    if len(documento) != 9:
        return False

    # Tabla de letras oficial
    letras_validas = "TRWAGMYFPDXBNJZSQVHLCKE"
    
    # Separamos letra final y parte numérica
    letra_usuario = documento[-1]
    parte_numerica = documento[:-1]

    # Gestión de NIEs (X, Y, Z se sustituyen por 0, 1, 2)
    if parte_numerica.startswith('X'):
        parte_numerica = '0' + parte_numerica[1:]
    elif parte_numerica.startswith('Y'):
        parte_numerica = '1' + parte_numerica[1:]
    elif parte_numerica.startswith('Z'):
        parte_numerica = '2' + parte_numerica[1:]

    # Si tras el reemplazo no son todo números, es inválido
    if not parte_numerica.isdigit():
        return False

    # Calculamos el resto de dividir por 23
    resto = int(parte_numerica) % 23
    
    # Comparamos la letra calculada con la que puso el usuario
    if letras_validas[resto] == letra_usuario:
        return True
    else:
        return False

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta_muy_segura'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'static', 'img', 'eventos')
app.config['RIFA_UPLOAD_FOLDER'] = os.path.join(basedir, 'static', 'img', 'rifas')

db.init_app(app)

# --- CONFIGURACIÓN DE LOGIN ---
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# --- ADMIN DECORATOR ---
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.es_admin:
            abort(403)  # Forbidden
        return f(*args, **kwargs)
    return decorated_function

# --- RUTAS PRINCIPALES ---

@app.route('/')
def index():
    # BocetoHome
    return render_template('index.html')

@app.route('/quienes-somos')
def quienes_somos():
    # BocetoUS (Misión, Historia, Equipo)
    return render_template('quienes_somos.html')

@app.route('/contacto')
def contacto():
    # BocetoContacto
    return render_template('contacto.html')

# --- RUTAS DE EVENTOS ---

@app.route('/eventos')
def eventos():
    lista_eventos = Evento.query.all()
    lista_rifas = Rifa.query.all()
    return render_template('eventos.html', eventos=lista_eventos, rifas=lista_rifas)

@app.route('/evento/<int:id>')
def ver_evento(id):
    # verEvento
    evento = Evento.query.get_or_404(id)
    return render_template('ver_evento.html', evento=evento)

@app.route('/rifa/<int:id>')
def ver_rifa(id):
    rifa = Rifa.query.get_or_404(id)
    return render_template('rifa.html', rifa=rifa)

@app.route('/rifa/<int:id>/participar', methods=['GET', 'POST'])
@login_required
def participar_rifa(id):
    rifa = Rifa.query.get_or_404(id)

    if request.method == 'POST':
        cantidad_boletos = int(request.form.get('cantidad', 1))
        metodo_pago = request.form.get('metodo_pago')

        # Aquí iría la lógica real de pago + guardar en BD (Modelo Boleto)
        flash(f'Has comprado {cantidad_boletos} boletos para la rifa "{rifa.nombre}" pagando con {metodo_pago}.')
        return redirect(url_for('dashboard'))

    return render_template('participar_rifa.html', rifa=rifa)

@app.route('/evento/comprar/<int:id_evento>', methods=['GET', 'POST'])
@login_required
def pago_entrada(id_evento):
    evento = Evento.query.get_or_404(id_evento)
    
    if request.method == 'POST':
        # 1. Recogemos datos básicos
        try:
            cantidad_entradas = int(request.form.get('cantidad', 1))
        except ValueError:
            cantidad_entradas = 1
            
        metodo_pago = request.form.get('metodo_pago')

        # 2. VALIDACIÓN DE TARJETA
        if metodo_pago == 'tarjeta':
            # Limpiamos espacios por si el usuario pone "1234 5678..."
            numero = request.form.get('tarjeta_numero', '').replace(' ', '')
            expiry = request.form.get('tarjeta_expiry', '').strip()
            cvv = request.form.get('tarjeta_cvv', '').strip()

            # A) Validar Número (Debe tener 16 dígitos exactos)
            if not re.match(r'^\d{16}$', numero):
                flash('❌ Error: El número de tarjeta no es válido (debe tener 16 dígitos).')
                return render_template('pago_entrada.html', evento=evento)

            # B) Validar CVV (Debe tener 3 dígitos)
            if not re.match(r'^\d{3}$', cvv):
                flash('❌ Error: El CVV es incorrecto (deben ser 3 dígitos).')
                return render_template('pago_entrada.html', evento=evento)

            # C) Validar Formato Fecha (MM/AA)
            if not re.match(r'^(0[1-9]|1[0-2])\/\d{2}$', expiry):
                flash('❌ Error: La fecha debe ser MM/AA (ej: 08/25).')
                return render_template('pago_entrada.html', evento=evento)

            # D) Validar que no esté Caducada
            try:
                mes, anio_corto = map(int, expiry.split('/'))
                anio_completo = 2000 + anio_corto # Convertir "25" en "2025"
                
                ahora = datetime.now()
                # Si el año es menor al actual, o es el mismo año pero el mes ya pasó
                if anio_completo < ahora.year or (anio_completo == ahora.year and mes < ahora.month):
                    flash('❌ Error: Su tarjeta está caducada.')
                    return render_template('pago_entrada.html', evento=evento)
            except:
                flash('❌ Error al validar la fecha de la tarjeta.')
                return render_template('pago_entrada.html', evento=evento)

        # 3. Si todo está correcto (o es Paypal/Bizum), procesamos la compra
        try:
            for _ in range(cantidad_entradas):
                # Generamos un código QR único simulado
                codigo_unico = f"ENTRADA-{evento.id}-{current_user.id}-{datetime.now().strftime('%f')}"
                
                nueva_entrada = Entrada(
                    precio=evento.precio,
                    id_evento=evento.id,
                    id_comprador=current_user.id,
                    codigo_qr=codigo_unico
                )
                db.session.add(nueva_entrada)
            
            db.session.commit()
            flash(f'✅ ¡Pago realizado con éxito! Has comprado {cantidad_entradas} entradas.')
            return redirect(url_for('dashboard'))
            
        except Exception as e:
            db.session.rollback()
            print(f"Error en base de datos: {e}")
            flash('❌ Hubo un error al procesar la compra. Inténtalo de nuevo.')
            return render_template('pago_entrada.html', evento=evento)
        
    return render_template('pago_entrada.html', evento=evento)

# --- RUTAS DE ADMINISTRACIÓN ---

@app.route('/admin/evento/crear', methods=['GET', 'POST'])
@login_required
@admin_required
def crear_evento():
    if request.method == 'POST':
        fecha_str = request.form.get('fecha')
        fecha = None
        if fecha_str:
            try:
                fecha = datetime.strptime(fecha_str, '%Y-%m-%dT%H:%M')
            except ValueError:
                fecha = None
        
        imagen_path = None
        if 'imagen' in request.files:
            file = request.files['imagen']
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                # Ensure filename is unique or handle collisions if necessary. 
                # For simplicity, we keep original filename but secure it.
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                filename = f"{timestamp}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                imagen_path = f"img/eventos/{filename}"

        nuevo_evento = Evento(
            nombre_evento=request.form.get('nombre'),
            localizacion=request.form.get('localizacion'),
            fecha=fecha,
            informacion=request.form.get('informacion'),
            imagen_evento=imagen_path,
            precio=float(request.form.get('precio', 0.0))
        )
        db.session.add(nuevo_evento)
        db.session.commit()
        flash('Evento creado exitosamente')
        return redirect(url_for('eventos'))
    return render_template('admin/crear_evento.html')

@app.route('/admin/evento/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_evento(id):
    evento = Evento.query.get_or_404(id)
    if request.method == 'POST':
        evento.nombre_evento = request.form.get('nombre')
        evento.localizacion = request.form.get('localizacion')
        evento.informacion = request.form.get('informacion')
        evento.precio = float(request.form.get('precio', 0.0))
        
        fecha_str = request.form.get('fecha')
        if fecha_str:
            try:
                evento.fecha = datetime.strptime(fecha_str, '%Y-%m-%dT%H:%M')
            except ValueError:
                pass
        
        if 'imagen' in request.files:
            file = request.files['imagen']
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                filename = f"{timestamp}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                evento.imagen_evento = f"img/eventos/{filename}"

        db.session.commit()
        flash('Evento actualizado')
        return redirect(url_for('ver_evento', id=id))
    return render_template('admin/editar_evento.html', evento=evento)

@app.route('/admin/evento/eliminar/confirmar/<int:id>')
@login_required
@admin_required
def confirmar_eliminar_evento(id):
    evento = Evento.query.get_or_404(id)
    return render_template('admin/confirmar_eliminar_evento.html', evento=evento)

@app.route('/admin/evento/eliminar/<int:id>', methods=['POST'])
@login_required
@admin_required
def eliminar_evento(id):
    evento = Evento.query.get_or_404(id)
    
    # 1. Eliminar imagen del sistema de archivos si existe
    if evento.imagen_evento:
        filename = os.path.basename(evento.imagen_evento)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        if os.path.exists(image_path):
            try:
                os.remove(image_path)
            except Exception as e:
                print(f"Error al eliminar imagen: {e}")

    # 2. Eliminar evento de la BD
    db.session.delete(evento)
    db.session.commit()
    flash('Evento e imagen eliminados correctamente')
    return redirect(url_for('eventos'))

@app.route('/admin/socios')
@login_required
@admin_required
def gestionar_socios():
    socios = Usuario.query.filter_by(es_socio=True).all()
    return render_template('admin/gestionar_socios.html', socios=socios)

@app.route('/baja-socio', methods=['POST'])
@login_required
def baja_socio():
    if current_user.es_socio:
        try:
            current_user.es_socio = False
            db.session.commit()
            flash('Has dado de baja tu suscripción de socio correctamente. Lamentamos verte partir.')
        except Exception as e:
            db.session.rollback()
            flash('Error al procesar la baja. Inténtalo de nuevo.')
    else:
        flash('No eras socio, por lo que no se ha realizado ninguna acción.')
        
    return redirect(url_for('dashboard'))

# --- GESTIÓN DE RIFAS (ADMIN) ---

@app.route('/admin/rifas')
@login_required
@admin_required
def gestionar_rifas():
    rifas = Rifa.query.all()
    return render_template('admin/gestionar_rifas.html', rifas=rifas)

@app.route('/admin/rifa/crear', methods=['GET', 'POST'])
@login_required
@admin_required
def crear_rifa():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        premio = request.form.get('premio')
        informacion = request.form.get('informacion')
        fecha_str = request.form.get('fecha')
        
        fecha_fin = None
        if fecha_str:
            try:
                fecha_fin = datetime.strptime(fecha_str, '%Y-%m-%dT%H:%M')
            except ValueError:
                pass

        imagen_path = None
        if 'imagen' in request.files:
            file = request.files['imagen']
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                filename = f"rifa_{timestamp}_{filename}"
                
                # Guardar en static/img/rifas usando config
                file.save(os.path.join(app.config['RIFA_UPLOAD_FOLDER'], filename))
                imagen_path = f"img/rifas/{filename}"

        nueva_rifa = Rifa(
            nombre=nombre,
            premio=premio,
            informacion=informacion,
            fecha_fin=fecha_fin,
            imagen=imagen_path
        )
        db.session.add(nueva_rifa)
        db.session.commit()
        flash('Rifa creada exitosamente')
        return redirect(url_for('gestionar_rifas'))
    return render_template('admin/crear_rifa.html')

@app.route('/admin/rifa/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_rifa(id):
    rifa = Rifa.query.get_or_404(id)
    if request.method == 'POST':
        rifa.nombre = request.form.get('nombre')
        rifa.premio = request.form.get('premio')
        rifa.informacion = request.form.get('informacion')
        
        fecha_str = request.form.get('fecha')
        if fecha_str:
            try:
                rifa.fecha_fin = datetime.strptime(fecha_str, '%Y-%m-%dT%H:%M')
            except ValueError:
                pass
        
        if 'imagen' in request.files:
            file = request.files['imagen']
            if file and file.filename != '':
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                filename = f"rifa_{timestamp}_{filename}"
                
                file.save(os.path.join(app.config['RIFA_UPLOAD_FOLDER'], filename))
                
                rifa.imagen = f"img/rifas/{filename}"

        db.session.commit()
        flash('Rifa actualizada')
        return redirect(url_for('gestionar_rifas'))
    return render_template('admin/editar_rifa.html', rifa=rifa)

@app.route('/admin/rifa/eliminar/<int:id>', methods=['POST'])
@login_required
@admin_required
def eliminar_rifa(id):
    rifa = Rifa.query.get_or_404(id)
    # Borrar imagen si existe
    if rifa.imagen:
        try:
            filename = os.path.basename(rifa.imagen)
            image_path = os.path.join(app.config['RIFA_UPLOAD_FOLDER'], filename)
            
            if os.path.exists(image_path):
                os.remove(image_path)
        except Exception as e:
            print(f"Error borrando imagen rifa: {e}")
            
    db.session.delete(rifa)
    db.session.commit()
    flash('Rifa eliminada')
    return redirect(url_for('gestionar_rifas'))

# --- RUTAS DE SOCIOS / DONACIONES ---

@app.route('/hazte-socio', methods=['GET', 'POST'])
def hazte_socio():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            flash('Debes iniciar sesión o registrarte para hacerte socio.')
            return redirect(url_for('login'))

        # Recoger datos básicos
        cantidad = request.form.get('cantidad')
        # Determinamos si viene de persona o empresa (asumimos persona por el ejemplo)
        periodo = request.form.get('periodo_persona')
        metodo_pago = request.form.get('metodo_pago_p')

        # --- VALIDACIÓN DE TARJETA (Igual que en Entradas) ---
        if metodo_pago == 'tarjeta':
            # Nota la '_p' al final de los campos
            numero = request.form.get('tarjeta_numero_p', '').replace(' ', '')
            expiry = request.form.get('tarjeta_expiry_p', '').strip()
            cvv = request.form.get('tarjeta_cvv_p', '').strip()

            # 1. Validar Número (16 dígitos)
            if not re.match(r'^\d{16}$', numero):
                flash('❌ Error: El número de tarjeta no es válido (debe tener 16 dígitos).')
                return render_template('hazte_socio.html')

            # 2. Validar CVV (3 dígitos)
            if not re.match(r'^\d{3}$', cvv):
                flash('❌ Error: El CVV es incorrecto (deben ser 3 dígitos).')
                return render_template('hazte_socio.html')

            # 3. Validar Formato Fecha (MM/AA)
            if not re.match(r'^(0[1-9]|1[0-2])\/\d{2}$', expiry):
                flash('❌ Error: La fecha de caducidad debe ser MM/AA (ej: 08/25).')
                return render_template('hazte_socio.html')

            # 4. Validar Caducidad Real
            try:
                mes, anio_corto = map(int, expiry.split('/'))
                anio_completo = 2000 + anio_corto
                ahora = datetime.now()
                
                if anio_completo < ahora.year or (anio_completo == ahora.year and mes < ahora.month):
                    flash('❌ Error: Su tarjeta está caducada.')
                    return render_template('hazte_socio.html')
            except:
                flash('❌ Error al validar la fecha de la tarjeta.')
                return render_template('hazte_socio.html')
        # --- FIN VALIDACIÓN ---

        # Si todo es correcto, guardamos en la base de datos
        try:
            current_user.es_socio = True
            db.session.commit()
            flash(f'¡Enhorabuena! Pago aceptado. Ya eres socio con una aportación de {cantidad}€ ({periodo}).')
            return redirect(url_for('dashboard'))
            
        except Exception as e:
            db.session.rollback()
            flash('Hubo un error al procesar tu solicitud en la base de datos.')
            return redirect(url_for('hazte_socio'))

    return render_template('hazte_socio.html')

@app.route('/hazte-voluntario', methods=['GET', 'POST'])
def hazte_voluntario():
    # BocetoHazteSocio_Persona y Empresa
    if request.method == 'POST':
        # Lógica para procesar el formulario de socio
        flash('Gracias por tu solicitud de socio. Te contactaremos pronto.')
        return redirect(url_for('index'))
    return render_template('hazte_voluntario.html')

@app.route('/donar')
def donar():
    if request.method == 'POST':
        # Lógica para procesar el formulario de donar
        flash('Gracias por tu donación.')
        return redirect(url_for('index'))
    return render_template('donar.html')

# --- RUTAS DE AUTENTICACIÓN (Tus rutas originales mejoradas) ---

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        email = request.form.get('email')
        # En el boceto registro hay nombre? Asumiremos que se usa parte del email o se añade el campo
        nombre = request.form.get('nombre', email.split('@')[0]) 
        password = request.form.get('password')
        password_repeat = request.form.get('password_repeat')
        
        if password != password_repeat:
            flash('Las contraseñas no coinciden')
            return render_template('registro.html')

        usuario_existente = Usuario.query.filter_by(correo_electronico=email).first()
        if usuario_existente:
            flash('El correo ya está registrado.')
            return redirect(url_for('registro'))

        nuevo_usuario = Usuario(
            nombre_usuario=nombre,
            correo_electronico=email,
            contrasena_hash=generate_password_hash(password, method='pbkdf2:sha256'),
            es_socio=False
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        login_user(nuevo_usuario)
        return redirect(url_for('dashboard'))

    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        usuario = Usuario.query.filter_by(correo_electronico=email).first()

        if usuario and check_password_hash(usuario.contrasena_hash, password):
            login_user(usuario)
            return redirect(url_for('dashboard'))
        else:
            flash('Email o contraseña incorrectos.')

    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    # Obtener las entradas del usuario
    entradas = Entrada.query.filter_by(id_comprador=current_user.id).all()
    return render_template('dashboard.html', user=current_user, entradas=entradas)

@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    if request.method == 'POST':
        nuevo_nombre = request.form.get('nombre')
        nuevo_email = request.form.get('email')
        nuevo_dni = request.form.get('dni')

        # 1. Validación de Email duplicado
        usuario_existente = Usuario.query.filter_by(correo_electronico=nuevo_email).first()
        if usuario_existente and usuario_existente.id != current_user.id:
            flash('Ese correo electrónico ya está en uso por otro usuario.')
            return redirect(url_for('editar_perfil'))

        # 2. NUEVA VALIDACIÓN DE DNI/NIF
        if nuevo_dni: # Solo validamos si el usuario escribió algo
            if not validar_dni_nie(nuevo_dni):
                flash('El DNI/NIE introducido no es válido. Revisa la letra.')
                return redirect(url_for('editar_perfil'))

        # Actualizar datos
        current_user.nombre_usuario = nuevo_nombre
        current_user.correo_electronico = nuevo_email
        # Guardamos el DNI siempre en mayúsculas para consistencia
        current_user.dni_nif = nuevo_dni.upper() if nuevo_dni else None
        
        try:
            db.session.commit()
            flash('Tus datos se han actualizado correctamente.')
            return redirect(url_for('dashboard'))
        except:
            db.session.rollback()
            flash('Error al actualizar la base de datos.')
            return redirect(url_for('editar_perfil'))

    return render_template('editar_perfil.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # --- DATOS DE PRUEBA (SOLO PARA VER QUE FUNCIONA) ---
        if not Evento.query.first():
            evento_demo = Evento(
                nombre_evento="Gala Benéfica James Bond",
                localizacion="Rotary Club Marbella",
                fecha=None, # Pon un datetime real aquí
                informacion="Una velada inolvidable..."
            )
            db.session.add(evento_demo)
            db.session.commit()
            
    app.run(debug=True)