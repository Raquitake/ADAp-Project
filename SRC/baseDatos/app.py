import os

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
    # pagoEntrada
    evento = Evento.query.get_or_404(id_evento)
    if request.method == 'POST':
        cantidad_entradas = int(request.form.get('cantidad', 1))
        # Aquí iría la lógica de pasarela de pago real
        # Por ahora simulamos la creación de entradas
        for _ in range(cantidad_entradas):
            nueva_entrada = Entrada(
                precio=20.0, # Precio ejemplo
                id_evento=evento.id,
                id_comprador=current_user.id,
                codigo_qr="QR_GENERADO_SIMULADO"
            )
            db.session.add(nueva_entrada)
        db.session.commit()
        flash('¡Entradas compradas con éxito!')
        return redirect(url_for('dashboard'))
        
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
            imagen_evento=imagen_path
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
                
                # Guardar en static/img
                save_dir = os.path.join(basedir, 'static', 'img')
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)
                    
                file.save(os.path.join(save_dir, filename))
                imagen_path = f"img/{filename}"

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
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                filename = f"rifa_{timestamp}_{filename}"
                save_dir = os.path.join(basedir, 'static', 'img')
                file.save(os.path.join(save_dir, filename))
                
                rifa.imagen = f"img/{filename}"

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
            full_path = os.path.join(basedir, 'static', rifa.imagen.replace('/', os.sep))
            if os.path.exists(full_path):
                os.remove(full_path)
        except Exception as e:
            print(f"Error borrando imagen rifa: {e}")
            
    db.session.delete(rifa)
    db.session.commit()
    flash('Rifa eliminada')
    return redirect(url_for('gestionar_rifas'))

# --- RUTAS DE SOCIOS / DONACIONES ---

@app.route('/hazte-socio', methods=['GET', 'POST'])
def hazte_socio():
    # BocetoHazteSocio_Persona y Empresa
    if request.method == 'POST':
        # Lógica para procesar el formulario de socio
        flash('Gracias por tu solicitud de socio. Te contactaremos pronto.')
        return redirect(url_for('index'))
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